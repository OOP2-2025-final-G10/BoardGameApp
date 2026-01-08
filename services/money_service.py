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

# 例：給料イベントの処理関数内
def handle_payday(user: User):
    if user.job:
        current_salary = user.job.salary
        
        # 1. お金を増やす
        user.money += current_salary
        
        # 2. 「前回の給料」として記録更新
        user.last_salary = current_salary
        
        print(f"{user.name}は給料 {current_salary}円を受け取りました。(前回給料を更新)")
    else:
        print(f"{user.name}は無職のため給料はありません。")