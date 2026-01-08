import uuid
from flask import Flask, request, redirect, url_for, render_template, session
from models.user import User

app = Flask(__name__)
app.secret_key = "secret_key"

users = {}

#参加画面
@app.route("/", methods=["GET"])
def index():
    is_registered = "user_id" in session
    return render_template("setup.html", is_registered=is_registered)

#ユーザー参加処理
@app.route("/", methods=["POST"])
def join():
    if "user_id" in session:
        return "", 204

    username = request.form.get("username")
    if not username:
        return "", 400

    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        name=username,
        money=50000,
        holdings={},
        job=None
    )

    users[user_id] = user
    session["user_id"] = user_id

    return "", 204

#ゲーム画面 未登録ユーザーであれば参加画面へリダイレクト
@app.route("/game")
def game():
    user_id = session.get("user_id")

    if not user_id or user_id not in users:
        return redirect(url_for("index"))

    user = users[user_id]
    return render_template("game.html", user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)