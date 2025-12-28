from models.spot import Spot
from models.vector2 import Vector2
import services.stock_price_service

class Map:
    def __init__(self, positions: list[Vector2]):
        stock_prices = services.stock_price_service.generate_stock_prices(len(positions))
        self.spots: list[Spot] = [
            Spot(spot_id=i, position=position, stock_prices=stock_prices[i])
            for i, position in enumerate(positions)
        ]

    def get_spot(self, spot_id: int) -> Spot:
        return self.spots[spot_id]
