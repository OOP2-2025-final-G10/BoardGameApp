from controllers.frontend_controller import FrontendController


class TurnService:
    def __init__(self):
        self.turn = 0

    def next_turn(self):
        self.turn += 1
        FrontendController.send_turn_change(self.turn)

    def get_current_turn(self):
        return self.turn
