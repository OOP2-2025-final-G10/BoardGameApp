class Stock:
    def __init__(self, stock_id: int, name: str, count: int = 0):
        self.stock_id = stock_id
        self.name = name
        self.count = count

    def to_dict(self):
        return {"stock_id": self.stock_id, "name": self.name, "count": self.count}