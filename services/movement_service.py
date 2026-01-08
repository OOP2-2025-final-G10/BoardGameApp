from typing import List
from models.spot import Spot
from controllers.frontend_controller import FrontendController


class MovementService:

    @staticmethod
    def move_piece(spots: List[Spot], to_spot_id: int) -> Spot:
        spot = spots[to_spot_id]

        FrontendController.send_scroll_position(spot.position)

        return spot
