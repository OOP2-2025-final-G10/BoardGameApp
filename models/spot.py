from typing import Tuple
from models.stock_prices import StockPrices
from models.vector2 import Vector2

class Spot:
    def __init__(self, spot_id: int, position: Vector2, stock_prices: StockPrices):
        self.spot_id = spot_id
        self.position = position
        self.stock_prices = stock_prices # 銘柄ごとの株価情報