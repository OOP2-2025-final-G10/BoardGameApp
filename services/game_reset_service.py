from models.db import get_db

class GameResetService:
    @staticmethod
    def reset_game():
        db = get_db()

        # ① 全ユーザー削除
        db.execute("DELETE FROM users")

        # ② ゲーム状態を初期状態へ
        db.execute("""
            UPDATE game_state
            SET
                status = 'waiting',
                turn_user_id = NULL,
                turn_number = 0
            WHERE id = 1
        """)

        db.commit()
        db.close()
