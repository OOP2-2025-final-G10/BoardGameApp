from models import db
from models.job import Job

class User:
    def __init__(self,id: str,spot_id: int,name: str,money: int,job: Job | None,holdings: dict[str, int] | None = None):
        self.user_id = id
        self.spot_id = spot_id
        self.name = name
        self.money = money
        self.job = job
        self.holdings = holdings or {}

    @classmethod
    def from_row(cls, row):
        job = Job.from_name(row["job"]) if row["job"] else None

        return cls(
            id=row["id"],
            spot_id=row["spot_id"],
            name=row["name"],
            money=row["money"],
            job=job
        )
    
    def save(self, db):
        db.execute(
            """
            UPDATE users
            SET money = ?, job = ?, spot_id = ?
            WHERE id = ?
            """,
            (
                self.money,
                self.job.name if self.job else None,
                self.spot_id,
                self.user_id
            )
        )


    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "spot_id": self.spot_id,
            "name": self.name,
            "money": self.money,
            "holdings": self.holdings,
            "job": self.job.to_dict() if self.job else None
        }