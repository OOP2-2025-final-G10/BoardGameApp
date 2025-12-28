from models.user import User
from controllers.frontend_controller import FrontendController


class MoneyService:

    @staticmethod
    def add(user: User, amount: int):
        before = user.money
        user.money += amount
        FrontendController.send_money_update(before, user.money)

    @staticmethod
    def subtract(user: User, amount: int):
        before = user.money
        user.money -= amount
        FrontendController.send_money_update(before, user.money)
