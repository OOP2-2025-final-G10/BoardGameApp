class Job:
    def __init__(self, name: str, salary: int):
        self.name = name
        self.salary = salary

    def to_dict(self):
        return {"name": self.name, "salary": self.salary}