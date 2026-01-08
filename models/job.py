class Job:
    def __init__(self, job_id: int, name: str, salary: int):
        self.job_id = job_id
        self.name = name
        self.salary = salary

    def to_dict(self):
        return {"job_id": self.job_id, "name": self.name, "salary": self.salary}
