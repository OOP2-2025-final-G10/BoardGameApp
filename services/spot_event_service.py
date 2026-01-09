class SpotEventService:

    @staticmethod
    def handle(user, db):
        """
        マス目に止まった後のイベント処理
        """
        spot = user.spot_id

        #マス目ごとのイベント定義
        user.money += 10000

        user.save(db)
