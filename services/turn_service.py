from controllers.frontend_controller import FrontendController


class TurnService:

    @staticmethod
    def next_turn(db):
        # 現在のターン情報
        state = db.execute("""
            SELECT turn_user_id, turn_number
            FROM game_state
            WHERE id = 1
        """).fetchone()

        # 全ユーザーを順序付きで取得
        users = db.execute("""
            SELECT id FROM users ORDER BY rowid ASC
        """).fetchall()

        if not users:
            return

        user_ids = [u["id"] for u in users]

        # 現在のユーザー位置
        current_index = user_ids.index(state["turn_user_id"])
        next_index = (current_index + 1) % len(user_ids)

        next_user_id = user_ids[next_index]

        # game_state 更新
        db.execute("""
            UPDATE game_state
            SET turn_user_id = ?, turn_number = ?
            WHERE id = 1
        """, (next_user_id, state["turn_number"] + 1))

