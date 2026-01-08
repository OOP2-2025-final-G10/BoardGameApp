from models.job import Job

class User:
    def __init__(self, id: int, name: str, money: int, holdings: dict[str, int], job: Job):
        self.user_id = id
        self.name = name
        self.money = money
        self.holdings = holdings
        self.job = job

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "money": self.money,
            "holdings": self.holdings,
            "job": self.job.to_dict() if self.job else None
        }
