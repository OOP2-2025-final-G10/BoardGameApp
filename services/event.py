from models.user import User
from models.job import Job
from controllers.frontend_controller import FrontendController


class Event:

    #所持金を変更する
    @staticmethod
    def change_money(user: User, amount: int):
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
        daily_prices: list[list[float]]
    ):
        """
        user: 対象となるユーザー
        stock_name: 銘柄名(stock_price_service.py の stock_names に準拠)
        amount: 購入する株数
        daily_prices: stock_price_service.pyのgenerate_stock_prices の戻り値をそのまま渡すこと

        戻り値:
            { "purchased": True, "symbol": str, "qty": int, "spent": int }
            または
            { "purchased": False, "reason": str }
        """

        stock_names = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]

        # --- 入力チェック ---
        if amount <= 0:
            return {"purchased": False, "reason": "invalid amount"}

        if stock_name not in stock_names:
            return {"purchased": False, "reason": "invalid stock name"}
        
        day = user.spot_id  # 現在のマス目を日数として扱う

        prices_today = daily_prices[day]
        if len(prices_today) != len(stock_names):
            return {"purchased": False, "reason": "price data corrupted"}

        # --- 株価取得 ---
        index = stock_names.index(stock_name)
        price = max(1, int(round(prices_today[index])))

        total_cost = price * amount

        # --- 資金チェック ---
        if user.money < total_cost:
            return {"purchased": False, "reason": "insufficient funds"}

        # --- 購入処理 ---
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
        daily_prices: list[list[float]]
    ):
        """
        user: 対象となるユーザー
        stock_name: 銘柄名
        amount: 売却する株数(-1で全株売却)
        daily_prices: generate_stock_prices の戻り値

        戻り値:
            { "sold": True, "symbol": str, "qty": int, "earned": int }
            または
            { "sold": False, "reason": str }
        """

        stock_names = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]

        # --- 入力チェック ---
        if amount <= 0:
            return {"sold": False, "reason": "invalid amount"}

        if stock_name not in stock_names:
            return {"sold": False, "reason": "invalid stock name"}

        # --- 保有チェック ---
        owned = user.holdings.get(stock_name, 0)
        if owned < amount:
            return {
                "sold": False,
                "reason": "not enough shares"
            }
        
        day = user.spot_id  # 現在のマス目を日数として扱う

         # --- 数量解釈 ---
        if amount == -1:
            sell_qty = owned
        elif amount > 0:
            if owned < amount:
                return {"sold": False, "reason": "not enough shares"}
            sell_qty = amount
        else:
            return {"sold": False, "reason": "invalid amount"}

        prices_today = daily_prices[day]
        if len(prices_today) != len(stock_names):
            return {"sold": False, "reason": "price data corrupted"}

        # --- 株価取得 ---
        index = stock_names.index(stock_name)
        price = max(1, int(round(prices_today[index])))

        total_gain = price * sell_qty

        # --- 売却処理 ---
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

