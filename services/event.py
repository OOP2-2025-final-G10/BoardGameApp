import json
from models.user import User
from models.job import Job
from controllers.frontend_controller import FrontendController


class UserEvent:

    #所持金を増加または減少させる
    @staticmethod
    def add_money(user: User, amount: int):
        user.money += amount

    #職業を変更する
    @staticmethod
    def change_job(user: User, new_job_name: str):
        user.job =  Job.from_name(new_job_name)

    #給料を支払う
    @staticmethod
    def give_salary(user: User):
        if not user.job:
            return
        user.money += user.job.salary
    
    #株を購入する
    @staticmethod
    def buy_stock(
        user: User,
        stock_name: str,
        amount: int,
        db
    ):
        stock_names = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]

        # --- 入力チェック ---
        if amount <= 0:
            return {"purchased": False, "reason": "不正な値です"}

        if stock_name not in stock_names:
            return {"purchased": False, "reason": "invalid stock name"}

        daily_prices = UserEvent.get_daily_prices(db)
        if not daily_prices:
            return {"purchased": False, "reason": "price data not found"}

        day = user.spot_id

        if day >= len(daily_prices):
            return {"purchased": False, "reason": "invalid day"}

        prices_today = daily_prices[day]
        if len(prices_today) != len(stock_names):
            return {"purchased": False, "reason": "price data corrupted"}

        index = stock_names.index(stock_name)
        price = max(1, int(round(prices_today[index])))

        total_cost = price * amount

        if user.money < total_cost:
            return {"purchased": False, "reason": "資金が不足しています"}

        user.money -= total_cost
        user.holdings[stock_name] = user.holdings.get(stock_name, 0) + amount

        return {
            "purchased": True,
            "symbol": stock_name,
            "qty": amount,
            "spent": total_cost
        }

    @staticmethod
    def sell_stock(
        user: User,
        stock_name: str,
        amount: int,
        db
    ):
        stock_names = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]
    
        if amount <= 0 and amount != -1:
            return {"sold": False, "reason": "不正な値です"}
    
        if stock_name not in stock_names:
            return {"sold": False, "reason": "invalid stock name"}
    
        owned = user.holdings.get(stock_name, 0)
        if owned == 0:
            return {"sold": False, "reason": "その株は保有していません"}
    
        daily_prices = UserEvent.get_daily_prices(db)
        if not daily_prices:
            return {"sold": False, "reason": "price data not found"}
    
        day = user.spot_id
        if day >= len(daily_prices):
            return {"sold": False, "reason": "invalid day"}
    
        prices_today = daily_prices[day]
        index = stock_names.index(stock_name)
        price = max(1, int(round(prices_today[index])))
    
        sell_qty = owned if amount == -1 else amount
        if owned < sell_qty:
            return {"sold": False, "reason": "保有数を超えています"}
    
        total_gain = price * sell_qty
    
        user.money += total_gain
        user.holdings[stock_name] -= sell_qty
    
        if user.holdings[stock_name] == 0:
            del user.holdings[stock_name]
    
        return {
            "sold": True,
            "symbol": stock_name,
            "qty": sell_qty,
            "earned": total_gain
        }


    @staticmethod
    def get_daily_prices(db):
        row = db.execute("""
            SELECT daily_prices
            FROM game_state
            WHERE id = 1
        """).fetchone()

        if not row or not row["daily_prices"]:
            return None

        return json.loads(row["daily_prices"])


