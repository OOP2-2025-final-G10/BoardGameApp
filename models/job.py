class Job:
    JOB_MASTER = {
        "会社員": {"job_id": 1, "salary": 150000},
        "医者": {"job_id": 2, "salary": 800000},
        "アルバイトリーダー": {"job_id": 3, "salary": 100000},
        "エンジニア": {"job_id": 4, "salary": 500000},
        "研究者": {"job_id": 5, "salary": 400000},
        "教員": {"job_id": 6, "salary": 350000},
        "公務員": {"job_id": 7, "salary": 300000},
        "経営者": {"job_id": 8, "salary": 1000000},
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
