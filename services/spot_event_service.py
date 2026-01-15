from services.event import UserEvent
import random

class SpotEventService:

    @staticmethod
    def handle(user, db):
        spot = user.spot_id

        # 株の銘柄リスト（必要に応じて使用）
        stock_names = ["東葉電気", "Novasystems", "関東食品", "南日本旅客鉄道", "林不動産レジデンシャル"]

        # 134マス目までのイベント定義
        match spot:
            # --- 第1ゾーン：スタート〜30マス ---
            case 1: # 職業マス
                UserEvent.change_job(user, "会社員")
            case 2: # 職業マス
                UserEvent.change_job(user, "医者")
            case 3: # 職業マス
                UserEvent.change_job(user, "アルバイトリーダー")
            case 4: # 職業マス
                UserEvent.change_job(user, "エンジニア")
            case 5: # 職業マス
                UserEvent.change_job(user, "研究者")
            case 6: # 職業マス
                UserEvent.change_job(user, "教員")
            case 7: # 職業マス
                UserEvent.change_job(user, "公務員")
            case 8: # 職業マス
                UserEvent.change_job(user, "経営者")
            case 9: # 全員止まる
                pass
            case 10: # 友人の引越しを手伝う
                UserEvent.add_money(user, 10000)
            case 11: # 深夜のテンションで謎の健康器具を買う
                UserEvent.subtract_money(user, 30000)
            case 12: # コンビニスイーツにハマる
                UserEvent.subtract_money(user, 5000)
            case 13: # マッチングアプリに登録する
                UserEvent.subtract_money(user, 10000)
            case 14:  # 実家の手伝いをしてお小遣いをもらう
                UserEvent.add_money(user, 10000)
            case 15: # 初任給で親にプレゼント
                UserEvent.subtract_money(user, 30000)
            case 16: # 同期と飲み会で意気投合
                pass
            case 17: # 満員電車で靴が片方なくなる
                UserEvent.subtract_money(user, 10000)
            case 18: # 資格試験に合格
                UserEvent.add_money(user, 50000)
            case 19: # 【給料日】
                pass
            case 20: # 週末にフェスへ行く
                UserEvent.subtract_money(user, 20000)
            case 21: # 迷い猫を保護して飼い主に感謝される
                UserEvent.add_money(user, 30000)
            case 22: # 寝坊して遅刻
                UserEvent.subtract_money(user, 10000)
            case 23: # ボーナスが出た！（給料の半額をもらう）
                if user.job:
                    bonus = user.job.salary // 2
                    UserEvent.add_money(user, bonus)
            case 24: # 衝動的に高い自転車を買う
                UserEvent.subtract_money(user, 100000)
            case 25: # サイクリングで健康になる（3マス進む）
                user.spot_id += 3
            case 26: # 自炊に失敗して結局外食
                UserEvent.subtract_money(user, 5000)
            case 27: # 路上ライブで投げ銭をもらう
                UserEvent.add_money(user, 2000)
            case 28: # クレジットカードの請求額に驚愕
                UserEvent.subtract_money(user, 50000)
            case 29: # 同窓会で昔の恋人に再会
                UserEvent.subtract_money(user, 30000)
            # 30マス目は空き（調整用）
            case 30:
                pass

            # --- 第2ゾーン：キャリア・結婚・マイホーム編（31〜80マス） ---
            case 31: # 【給料日】
                pass
            case 32: # 車を購入する
                UserEvent.subtract_money(user, 500000)
            case 33: # ドライブデートに行く
                UserEvent.subtract_money(user, 30000)
            case 34: # 営業成績トップで表彰
                UserEvent.add_money(user, 300000)
            case 35: # ストレスで暴飲暴食
                UserEvent.subtract_money(user, 20000)
            case 36: # 友人の結婚式ラッシュ
                UserEvent.subtract_money(user, 100000)
            case 37: # 【ストップ！結婚マス】
                # 全員からご祝儀3万円ずつもらう（簡易実装：参加者を4人と仮定して他3人から貰う）
                UserEvent.add_money(user, 300000)
            case 38: # 旅行でハワイへ
                UserEvent.subtract_money(user, 500000)
            case 39: # 手料理が美味しい（2マス進む）
                user.spot_id += 2
            case 40: # 喧嘩して家出する（1回休み）
                pass
            case 41: # 【給料日】
                pass
            case 42: # 子犬を飼い始める
                UserEvent.subtract_money(user, 200000)
            case 43: # 宝くじ（ミニロト）に当選！
                UserEvent.add_money(user, 1000000)
            case 44: # 親知らずを抜く
                UserEvent.subtract_money(user, 10000)
            case 45: # 副業が軌道に乗る
                UserEvent.add_money(user, 200000)
            case 46: # ネット詐欺にあいかける
                UserEvent.subtract_money(user, 10000)
            case 47: # 近所の騒音トラブルに巻き込まれる
                UserEvent.subtract_money(user, 300000)
            case 48: # 趣味のキャンプ道具を揃える
                UserEvent.subtract_money(user, 150000)
            case 49: # YouTuberデビュー。意外と再生される
                UserEvent.add_money(user, 50000)
            case 50: # 犬の糞を踏む
                UserEvent.subtract_money(user, 30000)
            case 51: # 税金の支払い（前回の給料の30%と仮定）
                tax = int(user.last_salary * 0.3)
                UserEvent.subtract_money(user, tax)
            case 52: # 家庭菜園のトマトが豊作
                UserEvent.add_money(user, 5000)
            case 53: # 子供が生まれる！
                UserEvent.add_money(user, 1000000)
            case 54: # 学資保険に加入する
                UserEvent.subtract_money(user, 50000)
            case 55: # 【給料日】
                pass
            case 56: # ゴルフを始める
                UserEvent.subtract_money(user, 200000)
            case 57: # ホールインワン達成！
                UserEvent.add_money(user, 300000)
            case 58: # ぎっくり腰になる（1回休み）
                pass
            case 59: # 温泉旅行で湯治する
                UserEvent.subtract_money(user, 50000)
            case 60: # 会社の業績悪化（今回は減給処理なしでメッセージのみ想定）
                pass
            case 61: # 転職の誘いが来る（給料アップボーナスとして処理）
                UserEvent.add_money(user, 100000)
            case 62: # 洗濯機が壊れて水浸し
                UserEvent.subtract_money(user, 150000)
            case 63: # 実家の蔵から骨董品発見
                UserEvent.add_money(user, 500000)
            case 64: # 老後のために投資を始める
                UserEvent.subtract_money(user, 100000)
            case 65: # 義母にマルチ勧誘される
                UserEvent.subtract_money(user, 200000)
            case 66: # 台風で屋根が飛ぶ
                UserEvent.subtract_money(user, 1000000)
            case 67: # 【給料日】
                pass
            case 68: # 勤続10年リフレッシュ休暇（2マス進む）
                user.spot_id += 2
            case 69: # 子供の教育費がかさむ
                UserEvent.subtract_money(user, 300000)
            case 70: # 子供がコンクールで優勝！
                UserEvent.add_money(user, 100000)
            case 71: # 地域の役員を押し付けられる
                pass
            case 72: # ふるさと納税の返礼品が大量に届く
                UserEvent.add_money(user, 30000)
            case 73: # 高級腕時計を買ってドヤる
                UserEvent.subtract_money(user, 1000000)
            case 74: # 腕時計を紛失（分岐等は未実装、メッセージのみ）
                pass
            case 75: # 児童虐待で警察に指導
                UserEvent.subtract_money(user, 300000)
            case 76: # 恋人にの誕生日にバッグを買う
                UserEvent.subtract_money(user, 200000)
            case 77: # 【給料日】
                pass
            case 78: # 人間ドックで再検査
                UserEvent.subtract_money(user, 50000)
            case 79: # 健康のためにジムに通う
                UserEvent.subtract_money(user, 100000)
            case 80: # マッチョになってモテ期到来
                # 全員から5万円もらう（他3人と仮定）
                UserEvent.add_money(user, 150000)

            # --- 第3ゾーン：波乱万丈・大逆転編（81〜130マス） ---
            case 81: # 【給料日】
                pass
            case 82: # 熟年離婚の危機
                UserEvent.subtract_money(user, 5000000)
            case 83: # 危機を乗り越え絆が深まる
                UserEvent.subtract_money(user, 1000000)
            case 84: # 会社が倒産！リストラ！
                UserEvent.add_money(user, 500000)
                UserEvent.change_job(user, "無職")
            case 85: # 蕎麦屋に投資
                UserEvent.subtract_money(user, 3000000)
            case 86: # 投資先の蕎麦屋が大繁盛！
                UserEvent.add_money(user, 5000000)
            case 87: # 投資先の蕎麦屋が潰れる
                UserEvent.subtract_money(user, 6000000)
            case 88: # 孫が生まれる
                UserEvent.subtract_money(user, 200000)
            case 89: # 孫にお小遣いをせびられる
                UserEvent.subtract_money(user, 50000)
            case 90: # 親戚にお金をせがまれる
                UserEvent.subtract_money(user, 500000)
            case 91: # カジノで全財産を賭ける（無一文）
                user.money = 0
            case 92: # 石油を掘り当てる
                UserEvent.add_money(user, 100000000)
            case 93: # コツコツ貯めた500円玉貯金を開封
                UserEvent.add_money(user, 300000)
            case 94: # 家庭菜園が巨大化してテレビ取材
                UserEvent.add_money(user, 50000)
            case 95: # 【給料日】
                pass
            case 96: # 富豪に恵んでもらう
                if user.money == 0:
                    UserEvent.add_money(user, 100000000)
            case 97: # 隕石が庭に落ちてくる
                UserEvent.add_money(user, 5000000)
            case 98: # 宇宙人と遭遇（3マス戻る）
                user.spot_id -= 3
            case 99: # 世界一周クルーズへ出発
                UserEvent.subtract_money(user, 3000000)
            case 100: # 船上で大富豪と仲良くなる（壺をもらう）
                pass
            case 101: # 実は壺が偽物だった
                UserEvent.subtract_money(user, 100000)
            case 102: # シロアリ被害で家が倒壊
                UserEvent.subtract_money(user, 10000000)
            case 103: # 選挙に出馬する
                UserEvent.subtract_money(user, 5000000)
            case 104: # 当選！政治家になる
                UserEvent.add_money(user, 10000000)
                # 政治家ジョブがあれば変更するが、今回はボーナスのみ
            case 105: # 【給料日】
                pass
            case 106: # 徳川埋蔵金を発見！
                UserEvent.add_money(user, 50000000)
            case 107: # 偽物だった
                UserEvent.subtract_money(user, 10000)
            case 108: # ユーチューバーの孫とコラボ
                UserEvent.add_money(user, 1000000)
            case 109: # 高齢者詐欺を撃退！
                UserEvent.add_money(user, 100000)
            case 110: # ゲートボール大会で優勝
                UserEvent.add_money(user, 30000)
            case 111: # 突然のモテ期、再び（養育費）
                UserEvent.subtract_money(user, 10000000)
            case 112: # 昔貸したお金が利子付きで返ってくる
                UserEvent.add_money(user, 1000000)
            case 113: # 豪邸をリフォームする
                UserEvent.subtract_money(user, 15000000)
            case 114: # 税務署の監査が入る（手持ちの半分没収）
                seize = user.money // 2
                UserEvent.subtract_money(user, seize)
            case 115: # 【給料日】
                pass
            case 116: # 名誉市民に選ばれる
                UserEvent.add_money(user, 3000000)
            case 117: # 若返りの薬を怪しい商人から買う
                UserEvent.subtract_money(user, 500000)
            case 118: # 薬の効果でお腹を下す
                UserEvent.subtract_money(user, 10000)
            case 119: # 全員にプレゼントを配る（3人に100万ずつと仮定）
                UserEvent.subtract_money(user, 3000000)
            case 120: # 全員から敬われる（3人から100万ずつと仮定）
                UserEvent.add_money(user, 3000000)
            case 121: # 開発したAIアプリが世界的な大ヒット！
                UserEvent.add_money(user, 50000000)
            case 122: # 自宅の庭から徳川埋蔵金がざくざく出てきた
                UserEvent.add_money(user, 45000000)
            case 123: # 昔買った絵画が、実は巨匠の作品だった
                UserEvent.add_money(user, 30000000)
            case 124: # 宇宙旅行のペアチケットが当選（換金）
                UserEvent.add_money(user, 20000000)
            case 125: # 【給料日】
                pass
            case 126: # 所有していた山林がリゾート開発地に選ばれた
                UserEvent.add_money(user, 35000000)
            case 127: # 仮想通貨が暴騰して「億り人」ならぬ「半億り人」に
                UserEvent.add_money(user, 50000000)
            case 128: # 後の夢、海外の古城を衝動買い
                UserEvent.subtract_money(user, 50000000)
            case 129: # 投資話が大失敗。財産が紙切れに
                UserEvent.subtract_money(user, 30000000)
            case 130: # 超豪華世界一周クルーズへ出発
                UserEvent.subtract_money(user, 15000000)
            case 131: # 豪邸の地下に巨大なシェルターを作ってしまった
                UserEvent.subtract_money(user, 20000000)
            case 132: # 孫や親戚全員に新車をプレゼントする
                UserEvent.subtract_money(user, 10000000)
            case 133: # 美術品のオークションで熱くなりすぎて落札
                UserEvent.subtract_money(user, 40000000)
            case 134: # 【ゴール！】
                # 順位判定やボーナスは別途ゲームロジックで処理を想定
                pass

        user.save(db)