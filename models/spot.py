from typing import List

class Spot:
    def __init__(self, spot_id: int):
        self.id = spot_id
        # 各株IDに対応する株価を格納
        self.stock_prices: List[float] = []

    def to_dict(self):
        return {"id": self.id, "stock_prices": self.stock_prices}