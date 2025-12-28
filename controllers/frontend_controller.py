class FrontendController:

    @staticmethod
    def send_scroll_position(position):
        x, y = position
        print(f"[Frontend] Scroll -> x={x}, y={y}")

    @staticmethod
    def send_money_update(before: int, after: int):
        diff = after - before
        print(f"[Frontend] Money -> {before} → {after} (diff={diff})")

    @staticmethod
    def send_turn_change(turn: int):
        print(f"[Frontend] Turn -> {turn}")
