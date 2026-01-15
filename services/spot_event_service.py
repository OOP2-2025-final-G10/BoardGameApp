from services.event import UserEvent

class SpotEventService:

    @staticmethod
    def handle(user, spot_id_before, db):

        stock_names = ["東葉電気", "Novasystems", "関東食品", "南日本旅客鉄道", "林不動産レジデンシャル"]

        #給料日ポイント
        salary_points = [5, 20, 31, 41, 55, 67, 81, 95]

        for point in salary_points:
            if spot_id_before < point <= user.spot_id:
                UserEvent.give_salary(user, db)

        #◯◯マス目にとまったら◯マス進める(特別マス)の処理
        if user.spot_id == 68:
            user.spot_id += 3

        #↓マス目ごとのイベント定義
        #0はスタート地点のため除外
        #以下は例なので、変更してください
        #134マス目まで実装してください
        match user.spot_id:
            #例
            case 1: #1マス目に止まった場合
                #所持金を増加させる
                UserEvent.add_money(user, 5000)
            case 2: #2マス目に止まった場合
                #所持金を減少させる
                UserEvent.subtract_money(user, 5000)
            case 3: #3マス目に止まった場合
                #職業を変更する
                UserEvent.change_job(user, "医者")
            case 4: #4マス目に止まった場合
                #給料を支払う
                UserEvent.give_salary(user)
            case 5:
                #株を無理やり購入させる例
                UserEvent.buy_stock(user, "東葉電気", 10, db)
            case 6:
                #株を無理やり売却させる例
                UserEvent.buy_stock(user, "Novasystems", 10, db)

        user.save(db)
