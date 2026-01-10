class Job:
    JOB_MASTER = {
        "会社員": {"job_id": 1, "salary": 3000},
        "医者": {"job_id": 2, "salary": 8000},
        "無職": {"job_id": 0, "salary": 0},
    }

    def __init__(self, job_id: int, name: str, salary: int):
        self.job_id = job_id
        self.name = name
        self.salary = salary

    @classmethod
    def from_name(cls, name: str | None):
        if not name:
            return None

        data = cls.JOB_MASTER.get(name)
        if not data:
            return None

        return cls(
            job_id=data["job_id"],
            name=name,
            salary=data["salary"]
        )

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "name": self.name,
            "salary": self.salary
        }
