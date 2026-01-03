import random
from noise import pnoise1
from models import Spot, Map

class GameMap:
    def __init__(self, spot_count: int, stock_count: int):
        self.spots = [Spot(i) for i in range(spot_count)]
        self.stock_count = stock_count
        # パーリンノイズのランダムシード（一回のゲームごとに変化）
        self.seed = random.random() * 100

    def generate_random_stock_prices(self):
        """
        パーリンノイズを用いて、マス目ごと・株IDごとの株価を決定する
        """
        # パラメータ（拡大率や振幅）
        scale = 0.1  # 数値が小さいほど、隣り合うマスの価格差が緩やかになる
        base_price = 1000.0  # 基準価格
        amplitude = 500.0   # 変動幅

        for spot in self.spots:
            prices = []
            for stock_id in range(self.stock_count):
                # パーリンノイズの算出
                # 入力値にstock_idを混ぜることで、銘柄ごとに異なる値動きにする
                noise_val = pnoise1(spot.id * scale + (stock_id * 50) + self.seed)
                
                # 株価の計算（基準値 + ノイズ値 * 変動幅）
                price = base_price + (noise_val * amplitude)
                prices.append(round(max(price, 100.0), 2)) # 最低価格を100に設定
            
            spot.stock_prices = prices

    def to_dict(self):
        return [spot.to_dict() for spot in self.spots]