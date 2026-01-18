# models/user.py
import json
from models.job import Job

class User:
    def __init__(
        self,
        id: str,
        spot_id: int,
        name: str,
        money: int,
        job: Job | None,
        holdings: dict[str, int] | None = None,
        last_salary: int = 0,
        goal_order: int | None = None
    ):
        self.user_id = id
        self.spot_id = spot_id
        self.name = name
        self.money = money
        self.job = job
        self.holdings = holdings or {}
        self.last_salary = last_salary
        self.goal_order = goal_order  # ★ ゴール順位（未ゴールは None）

    @classmethod
    def from_row(cls, row):
        # holdings（後方互換・安全）
        holdings = {}
        if "holdings" in row.keys() and row["holdings"]:
            try:
                holdings = json.loads(row["holdings"])
            except Exception:
                holdings = {}

        return cls(
            id=row["id"],
            spot_id=row["spot_id"],
            name=row["name"],
            money=row["money"],
            job=Job.from_name(row["job"]),
            holdings=holdings,
            goal_order=row["goal_order"] if "goal_order" in row.keys() else None
        )

    def save(self, db):
        db.execute(
            """
            UPDATE users
            SET
                money = ?,
                job = ?,
                spot_id = ?,
                holdings = ?,
                goal_order = ?
            WHERE id = ?
            """,
            (
                self.money,
                self.job.name if self.job else None,
                self.spot_id,
                json.dumps(self.holdings, ensure_ascii=False),
                self.goal_order,          # ★ 保存
                self.user_id
            )
        )

    @staticmethod
    def get_by_id(db, user_id: str):
        row = db.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        if not row:
            return None

        return User.from_row(row)

    @property
    def is_goal(self) -> bool:
        """ゴール済みかどうか（唯一の正解判定）"""
        return self.goal_order is not None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "money": self.money,
            "spot_id": self.spot_id,
            "job": self.job.to_dict() if self.job else None,
            "holdings": self.holdings,
            "last_salary": self.last_salary,
            "goal_order": self.goal_order,   # ★ フロント通知用
            "is_goal": self.is_goal           # ★ フロント判定を簡単に
        }
