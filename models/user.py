from numpy import long

from models.job import Job


class User:
    def __init__(self, name: str, money: long, holdings: dict[str, int], job: Job):
        self.name = name
        self.money = money
        self.holdings = holdings
        self.job = job