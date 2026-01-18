class TurnService:

    @staticmethod
    def next_turn(db):
        # 現在のターン情報
        state = db.execute("""
            SELECT turn_user_id, turn_number
            FROM game_state
            WHERE id = 1
        """).fetchone()

        current_user_id = state["turn_user_id"]

        # ★ 未ゴールユーザーのみ取得
        users = db.execute("""
            SELECT id
            FROM users
            WHERE goal_order IS NULL
            ORDER BY rowid ASC
        """).fetchall()


        # 全員ゴール済みなら何もしない
        if not users:
            return

        user_ids = [u["id"] for u in users]

        # 現在ユーザーがゴール済みの場合も考慮
        if current_user_id in user_ids:
            index = user_ids.index(current_user_id)
            next_index = (index + 1) % len(user_ids)
        else:
            # 現在ユーザーがゴールしていたら先頭へ
            next_index = 0

        next_user_id = user_ids[next_index]

        # game_state 更新
        db.execute("""
            UPDATE game_state
            SET turn_user_id = ?, turn_number = ?
            WHERE id = 1
        """, (
            next_user_id,
            state["turn_number"] + 1
        ))
