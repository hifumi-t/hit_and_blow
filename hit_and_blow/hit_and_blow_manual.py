# モジュールインポート，URL，プレイヤー情報の辞書登録
import requests
from typing import Tuple

class HitAndBlow:

    def __init__(self, i_am="C") -> None:
        self.URL = "https://damp-earth-70561.herokuapp.com"
        self.session = requests.Session()
        self.players = {"C":"290d6313-c662-45b6-82d6-6afb631ade08", 
                    "C2":"3cd613ef-a0c0-447c-bc23-81dcf1648be9"}
        self.i_am = i_am
        self.room_id = ""
        self.table_result = {}

    def get_room(self) -> dict:
        """指定した対戦部屋情報の取得

        :rtype: dict
        :return: 部屋の情報{
                            "id": int,
                            "state": int,
                            "player1": "string",
                            "player2": "string"
                            }
        """
        url_get_room = self.URL + "/rooms/" + str(self.room_id)
        result = self.session.get(url_get_room)
        return result.json()

    def input_roomID(self) -> int:
        """部屋IDの入力

        :rtype: int
        :return: ルームID
        """
        self.room_id = input("入室したい対戦部屋のIDを入力してください -->>")
        self.room_id = int(self.room_id)
        return self.room_id

    def check_room(self) -> bool:
        """部屋の情報を取得して，状況を返す

        :rtype: bool
        :return: 入れる部屋かどうか
        """
        get_room_result = self.get_room()
        if get_room_result["state"] == -1:
            print("部屋には誰もいません")
            return True
        elif get_room_result["state"] == 1:
            print("{}が待機しています".format(get_room_result["player1"]))
            return True
        else:
            print("すでに部屋が満席です．別の部屋IDを入力してください")
            return False

    def ask_enter_room(self) -> bool:
        """部屋に入室するか選択する

        :rtype: bool
        :return: 部屋に入るならTrue
        """
        while True:
            ans = input("入室しますか？[y/n] -->>")
            if ans == "y":
                return True
            elif ans == "n":
                return False
            else:
                print("y/n以外の入力がされました．入力をやり直してください")

    def enter_room(self) -> None:
        """対戦部屋へユーザーを登録

        :rtype: None
        :return: なし
        """
        headers = {"Content-Type" : "application/json"}
        url_enter_room = self.URL + "/rooms"
        post_data = {
            "player_id": self.players[self.i_am],
            "room_id": self.room_id
            }
        self.session.post(url_enter_room, headers=headers, json=post_data)
        print("入室しました")

    def input_hidden(self) -> str:
        """相手が当てる数字を登録する

        :rtype: str
        :return: 相手が当てる数字
        """
        self.hidden_number = input("相手に当てさせる番号を入力してください -->>")
        return self.hidden_number

    def post_hidden(self) -> str:
        """相手が当てる数字をサーバーに送る

        :rtype: str
        :return: 相手が当てる数字
        """
        headers = {"Content-Type" : "application/json"}
        url_get_table = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/hidden"
        
        while True:
            self.hidden_number = self.input_hidden()
            post_data = {
                "player_id": self.players[self.i_am],
                "hidden_number": self.hidden_number
            }
            result_post = self.session.post(url_get_table, headers=headers, json=post_data)
            if result_post.status_code == 200:
                print(f"{self.hidden_number}を相手に当ててもらいます")
                return self.hidden_number
            else:
                print("無効な入力がされました")

    def run_first_half(self) -> Tuple[int, str]:
        """プログラム前半（ID入力から相手が当てる数字を入力まで）
        
        :rtype: Tuple[int, str]
        :return: 入室したルームID，相手が当てる数字
        """
        enter = ""
        while enter != True: # 部屋に入るまで繰り返す
            room = ""
            while room != True: # 入れる部屋を選ぶまで繰り返す
                self.room_id = self.input_roomID()
                room = self.check_room()
            enter = self.ask_enter_room()
        self.enter_room()
        get_room_result = self.get_room()
        while get_room_result["state"] != 2:
            get_room_result = self.get_room()
        self.hidden_number = self.post_hidden()
        return self.room_id, self.hidden_number

    def get_table(self) -> dict:
        """対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する

        :rtype: dict
        :return: 対戦情報テーブル{
                    "room_id": int,
                    "state": int,
                    "now_player": "string",
                    "table": [
                        {
                        "guess": "string",
                        "hit": int,
                        "blow": int
                        }
                    ],
                    "opponent_table": [
                        {
                        "guess": "string",
                        "hit": int,
                        "blow": int
                        }
                    ],
                    "winner": "string",
                    "game_end_count": int
                    }
        """
        url_get_table =  self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/table"
        self.table_result = self.session.get(url_get_table)
        return self.table_result.json()

    def check_win(self) -> bool:
        """勝敗が決まったかチェック

        :rtype: bool
        :return: 勝敗が続くならTrue
        """
        if self.table_result["state"] == 2:
            return True # →ゲーム続行
        else:
            return False # →ゲーム終了

    def check_turn(self) -> bool:
        """自分のターンかチェック

        :rtype: bool
        :return: 自分のターンならTrue
        """
        if self.table_result["now_player"] == self.i_am:
            return True # →自分のターン
        else:
            return False # →相手のターン

    def end_game(self) -> None:
        """ゲーム終了

        :rtype: None
        :return: なし
        """
        if self.table_result["winner"] == self.i_am:
            print("あなたの勝ちです！おめでとう！")
        elif self.table_result["winner"] == None:
            print("引き分けです")
        else:
            print("あなたの負けです...")

    def post_guess(self) -> None:
        """推測した数字を登録する

        :rtype: None
        :return: なし
        """
        headers = {"Content-Type" : "application/json"}
        url_post_guess = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/table/guesses"
        post_data = {
            "player_id": self.players[self.i_am],
            "guess": input("相手の番号を推測して入力してください -->>")
        }
        self.session.post(url_post_guess, headers=headers, json=post_data)

    def run_second_half(self) -> None:
        """"
        プログラム後半

        :rtype: None
        :return: なし
        """
        while True: # 無限ループ
            turn = False
            while turn != True: # 自分のターンじゃない間ずっと
                self.table_result = self.get_table()
                if self.check_win() == False: # 勝者がいたらゲームを終わる
                    self.end_game()
                    return
                else: # 勝者がいないならゲーム続行．自分のターンかチェックするループを回す．
                    turn = self.check_turn()
            # ↓自分のターンなら
            self.post_guess()
            self.table_result = self.get_table()
            print(self.table_result["table"][-1])

def main():
    runner = HitAndBlow(i_am="C")
    runner.run_first_half()
    runner.run_second_half()

if __name__ == "__main__":
    main()