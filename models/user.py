from typing import List
from .job import Job
from .stock import Stock

class User:
    def __init__(self, name: str, initial_money: int):
        self.name = name
        self.money = initial_money
        self.holdings: List[Stock] = []
        self.job: Job = None

    def to_dict(self):
        return {
            "name": self.name,
            "money": self.money,
            "holdings": [s.to_dict() for s in self.holdings],
            "job": self.job.to_dict() if self.job else None
        }