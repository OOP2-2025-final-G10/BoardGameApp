from typing import Tuple
from models.vector2 import Vector2

class Spot:
    def __init__(self, spot_id: int, position: Vector2, stock_prices: list[float]):
        self.spot_id = spot_id
        self.position = position
        self.stock_prices = stock_prices #銘柄ごと
