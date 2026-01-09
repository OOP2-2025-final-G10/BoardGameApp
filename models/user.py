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
        holdings: dict[str, int] | None = None
    ):
        self.user_id = id
        self.spot_id = spot_id
        self.name = name
        self.money = money
        self.job = job
        self.holdings = holdings or {}

    @classmethod
    def from_row(cls, row):
        # sqlite3.Row は dict.get を持たないので安全に取得する
        try:
            raw = row["holdings"]  # カラムがあれば値（TEXT または None）が返る
        except KeyError:
            # holdings カラムが存在しない場合は空で初期化
            raw = None

        holdings = {}
        if raw:
            try:
                holdings = json.loads(raw) if isinstance(raw, str) else (raw or {})
            except Exception:
                # パースに失敗したら空 dict にフォールバック
                holdings = {}

        return cls(
            row["id"],                 # id
            row["spot_id"],            # spot_id
            row["name"],               # name
            row["money"],              # money
            Job.from_name(row["job"]), # job
            holdings                   # holdings
        )

    def save(self, db):
        db.execute(
            """
            UPDATE users
            SET
                money = ?,
                job = ?,
                spot_id = ?,
                holdings = ?
            WHERE id = ?
            """,
            (
                self.money,
                self.job.name if self.job else None,
                self.spot_id,
                json.dumps(self.holdings, ensure_ascii=False),
                self.user_id
            )
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "money": self.money,
            "spot_id": self.spot_id,
            "job": self.job.to_dict() if self.job else None,
            "holdings": self.holdings
        }
