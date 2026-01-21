import uuid
import json
from models import user
from services.event import UserEvent
from services.stock_price_service import generate_stock_prices
from flask import Flask, request, redirect, url_for, render_template, session, Response
from models.user import User
from models.db import get_db
from services.roulette_service import RouletteService
from services.spot_event_service import SpotEventService
from services.turn_service import TurnService
from flask import jsonify

app = Flask(__name__)
app.secret_key = "secret_key"

total_days = 134 #ゲーム全体の日数(マス目の総数)
previous_days = 50 #ゲーム開始前の日数(株価表示用)

users = {}

def init_db():
    db = get_db()

    db.execute("DROP TABLE IF EXISTS users")
    db.execute("DROP TABLE IF EXISTS game_state")

    db.execute("""
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            money INTEGER NOT NULL,
            job TEXT,
            spot_id INTEGER NOT NULL DEFAULT 0,
            is_ready INTEGER NOT NULL DEFAULT 0,
            holdings TEXT DEFAULT '{}',
            goal_order INTEGER          -- ゴール順位（未到達はNULL）
        )
    """)

    db.execute("""
        CREATE TABLE game_state (
            id INTEGER PRIMARY KEY,
            status TEXT NOT NULL,
            turn_user_id TEXT,
            turn_number INTEGER NOT NULL,
            daily_prices TEXT,
            goal_count INTEGER NOT NULL DEFAULT 0
        )
    """)

    db.execute("""
        INSERT INTO game_state
        (id, status, turn_user_id, turn_number, daily_prices, goal_count)
        VALUES (1, 'waiting', NULL, 0, NULL, 0)
    """)

    db.commit()
    db.close()


#セッションリセット用
@app.route("/reset")
def reset_session():
    session.clear()
    init_db()
    return redirect(url_for("index"))

#参加画面
@app.route("/", methods=["GET"])
def index():
    is_registered = "user_id" in session
    username = None

    if is_registered:
        db = get_db()
        user = db.execute(
            "SELECT name FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()
        db.close()
        if user:
            username = user["name"]
            return redirect(url_for("game"))

    return render_template(
        "setup.html",
        is_registered=is_registered,
        username=username
    )


#ユーザー参加処理
@app.route("/", methods=["POST"])
def join():
    if "user_id" in session:
        return "", 204

    username = request.form.get("username")
    if not username:
        return "", 400

    user_id = str(uuid.uuid4())

    db = get_db()
    db.execute(
        """
        INSERT INTO users (id, name, money, job, spot_id, holdings)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, username, 50000, None, 0, "{}")
    )
    db.commit()
    db.close()

    session["user_id"] = user_id
    return "", 204


#ゲーム画面 未登録ユーザーであれば参加画面へリダイレクト
@app.route("/game")
def game():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    db = get_db()

    user_row = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if not user_row:
        session.clear()
        db.close()
        return redirect(url_for("index"))

    state_row = db.execute(
        """
        SELECT status, turn_user_id
        FROM game_state
        WHERE id = 1
        """
    ).fetchone()


    is_my_turn = (state_row["turn_user_id"] == user_id)

    db.close()

    if not state_row or state_row["status"] != "playing":
        return redirect(url_for("index"))

    user = User.from_row(user_row)
    return render_template("game.html", user=user, is_my_turn=is_my_turn, users=users)




@app.route("/members")
def members():
    db = get_db()
    users = db.execute("SELECT name, is_ready FROM users").fetchall()
    state_row = db.execute("SELECT status FROM game_state WHERE id = 1").fetchone()
    db.close()

    status = state_row["status"] if state_row else "waiting"

    # セッションに user_id があるかで登録済み判定を返す
    is_registered = "user_id" in session and session.get("user_id") is not None

    return {
        "members": [
            {"name": u["name"], "ready": bool(u["is_ready"])}
            for u in users
        ],
        "status": status,
        "is_registered": bool(is_registered)
    }



@app.route("/ready", methods=["POST"])
def ready():
    user_id = session.get("user_id")
    if not user_id:
        return "", 403

    db = get_db()

    # 自分を ready にする
    db.execute(
        "UPDATE users SET is_ready = 1 WHERE id = ?",
        (user_id,)
    )

    # 全員が ready か確認
    total = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    ready = db.execute(
        "SELECT COUNT(*) FROM users WHERE is_ready = 1"
    ).fetchone()[0]

    if total > 0 and total == ready:
        first_user = db.execute(
            "SELECT id FROM users ORDER BY rowid ASC LIMIT 1"
        ).fetchone()

        daily_prices = generate_stock_prices(T=total_days + previous_days)
        daily_prices_json = json.dumps(daily_prices)

        db.execute("""
            UPDATE game_state
            SET status = 'playing',
                turn_user_id = ?,
                turn_number = 1,
                daily_prices = ?
            WHERE id = 1
        """, (first_user["id"], daily_prices_json))

    db.commit()
    db.close()

    return "", 204

@app.route("/roulette/stream")
def roulette_stream():
    user_id = session.get("user_id")
    if not user_id:
        return "", 403

    db = get_db()
    try:
        user = db.execute("""
            SELECT goal_order
            FROM users
            WHERE id = ?
        """, (user_id,)).fetchone()

        state = db.execute("""
            SELECT turn_user_id
            FROM game_state
            WHERE id = 1
        """).fetchone()

        # ★ ゴール済み or 自分のターンでない場合は即拒否
        if user["goal_order"] is not None:
            return "", 403

        if state["turn_user_id"] != user_id:
            return "", 403
    finally:
        db.close()

    def event_stream():
        for angle in RouletteService.spin_stream():
            yield f"data:{angle}\n\n"

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/api/roulette/result")
def roulette_result():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "unauthorized"}, 403

    db = get_db()
    try:
        state = db.execute("""
            SELECT turn_user_id, goal_count
            FROM game_state
            WHERE id = 1
        """).fetchone()

        if not state or state["turn_user_id"] != user_id:
            return {"error": "not your turn"}, 403

        user = User.get_by_id(db, user_id)

        # ★ すでにゴールしているユーザーは不可
        if user.goal_order is not None:
            return {"error": "already_goal"}, 403

        step = RouletteService.consume_result()

        spot_id_before = user.spot_id
        
        user.spot_id += step  
        
        # 2. 移動後の位置(user.spot_id)を使ってイベント判定を行う
        SpotEventService.handle(user, spot_id_before, db)

        reached_goal = False
        rank = None
        prize = 0

        # ★ ゴール到達「瞬間」だけ処理
        if user.spot_id >= 135:
            user.spot_id = 135
            reached_goal = True
            rank = state["goal_count"] + 1

            user.goal_order = rank
            UserEvent.sell_all_stocks(user, db)
            prize = UserEvent.goal_prize_for_rank(rank)
            if prize:
                user.money += prize

            db.execute("""
                UPDATE game_state
                SET goal_count = goal_count + 1
                WHERE id = 1
            """)

        user.save(db)

        TurnService.next_turn(db)
        db.commit()

        return {
            "step": step,
            "spot_id": user.spot_id,
            "goal": reached_goal,
            "rank": rank,
            "prize": prize
        }
    finally:
        db.close()


@app.route("/api/users")
def api_users():
    db = get_db()
    rows = db.execute(
        "SELECT id, name FROM users"
    ).fetchall()
    db.close()

    return jsonify({
        "users": [
            {
                "user_id": r["id"],
                "name": r["name"]
            }
            for r in rows
        ]
    })


@app.route("/api/user/<user_id>")
def api_user_detail(user_id):
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    db.close()

    if not row:
        return {"error": "not found"}, 404

    user = User.from_row(row)
    return user.to_dict()

@app.route("/api/game_state")
def api_game_state():
    db = get_db()
    row = db.execute("""
        SELECT status, turn_user_id, turn_number
        FROM game_state
        WHERE id = 1
    """).fetchone()
    db.close()

    if not row:
        return {"error": "game_state not found"}, 404

    return {
        "status": row["status"],
        "turn_user_id": row["turn_user_id"],
        "turn_number": row["turn_number"]
    }

@app.post("/api/stock/buy")
def buy_stock():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "unauthorized"}, 403

    db = get_db()
    data = request.json

    user = User.get_by_id(db, user_id)

    result = UserEvent.buy_stock(
        user=user,
        stock_name=data["stock_name"],
        amount=int(data["amount"]),
        db=db
    )

    user.save(db)
    db.commit()
    db.close()

    return jsonify(result)


@app.post("/api/stock/sell")
def sell_stock():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "unauthorized"}, 403

    db = get_db()
    data = request.json

    user = User.get_by_id(db, user_id)

    result = UserEvent.sell_stock(
        user=user,
        stock_name=data["stock_name"],
        amount=int(data["amount"]),
        db=db
    )

    user.save(db)
    db.commit()
    db.close()

    return jsonify(result)

def get_daily_prices(db):
    row = db.execute("""
        SELECT daily_prices
        FROM game_state
        WHERE id = 1
    """).fetchone()
    if not row or not row["daily_prices"]:
        return None
    return json.loads(row["daily_prices"])

@app.route("/api/stock/prices")
def api_stock_prices():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "unauthorized"}, 403

    db = get_db()

    user_row = db.execute(
        "SELECT spot_id FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    state_row = db.execute(
        "SELECT daily_prices FROM game_state WHERE id = 1"
    ).fetchone()

    db.close()

    if not user_row or not state_row or not state_row["daily_prices"]:
        return {"error": "data not found"}, 404

    spot_id = user_row["spot_id"]
    daily_prices = json.loads(state_row["daily_prices"])

    stock_names = ["東葉電気", "Novasystems", "関東食品", "南日本旅客鉄道", "林不動産レジデンシャル"]

    sliced = daily_prices[:spot_id + previous_days + 1]

    result = {
        name: [day[i] for day in sliced]
        for i, name in enumerate(stock_names)
    }

    return jsonify({
        "days": list(range(len(sliced))),
        "prices": result
    })

@app.route("/api/game_pieces")
def game_pieces():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, spot_id
        FROM users
    """)
    rows = cur.fetchall()

    players = {}
    for row in rows:
        players[row["id"]] = row["spot_id"]

    return jsonify(players)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
