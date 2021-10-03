# モジュールインポート，URL，プレイヤー情報の辞書登録
import itertools
import requests
import random
import numpy as np
from typing import List, Tuple, Union

class HitAndBlow:

    def __init__(self, i_am="C", strength=100) -> None:
        self.URL = "https://damp-earth-70561.herokuapp.com"
        self.session = requests.Session()
        self.num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        self.players = {"C":"290d6313-c662-45b6-82d6-6afb631ade08", 
                    "C2":"3cd613ef-a0c0-447c-bc23-81dcf1648be9"}
        self.i_am = i_am
        self.room_id = ""
        self.table_result = {}
        self.guess = ""
        self.answer = ""
        self.guess_number = "12345"
        self.strength = strength

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
        hidden = random.sample(self.num_list, 5)
        self.hidden_number = hidden[0]+hidden[1]+hidden[2]+hidden[3]+hidden[4]
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

    #----------------------------------アルゴリズム
    def hit_blow(self) -> List[Union[int, int]]:
        """予測と正解からヒットとブローの数を返す

        :rtype: List[int, int]
        :return: [ヒット, ブロー]
        """
        hit = 0
        blow = 0
        for i in range(5):
            if self.guess_number[i] == self.ans[i]:
                hit += 1
            elif self.guess_number[i] in self.ans:
                    blow += 1
        return [hit, blow]

    def make_ans_list(self) -> list:
        """初期正解候補を作る

        :rtype: list
        :return: 初期正解候補
        """
        ans_list_tuple = list(itertools.permutations(self.num_list, 5))
        self.ans_list = []
        for i in ans_list_tuple:
            self.ans_list.append(i[0]+i[1]+i[2]+i[3]+i[4])
        return self.ans_list

    def narrow_ans_list(self) -> list:
        """正解候補を絞る

        :rtype: list
        :return: 正解候補
        """
        new_ans_list = []
        length = len(self.ans_list)
        for self.ans in self.ans_list[:length+1]:
            h_b = self.hit_blow()
            lot = random.randint(0,100)
            if h_b == self.result: # 結果と一致するなら
                new_ans_list.append(self.ans) # 候補リストに加える
            elif h_b != self.result and lot > self.strength: # 結果と違うとしても一定確率で
                new_ans_list.append(self.ans) # 候補リストに加える
            else: # 結果と一致しないなら
                pass # なにもしない
        self.ans_list = new_ans_list # できた正解候補をもとのリストと置き換える
        return self.ans_list

    def get_result(self) -> Tuple[dict, List[Union[int, int]]]:
        """テーブルからヒットとブローの結果を返す

        :rtype: tuple[dict, List[int, int]]
        :return: テーブル，
        """
        self.table = self.get_table()
        self.result = [self.table["table"][-1]["hit"], self.table["table"][-1]["blow"]]
        return self.table, self.result
    #---------------------------------

    def post_guess(self) -> None:
        """推測した数字を登録する

        :rtype: None
        :return: なし
        """
        headers = {"Content-Type" : "application/json"}
        url_post_guess = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/table/guesses"
        post_data = {"player_id": self.players[self.i_am],"guess": self.guess_number}
        self.session.post(url_post_guess, headers=headers, json=post_data)

    def run_second_half(self) -> None:
        """"
        プログラム後半

        :rtype: None
        :return: なし
        """
        # self.guess_number = "12345"
        ans_list = self.make_ans_list()
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
            table, result = self.get_result()
            ans_list = self.narrow_ans_list()
            self.guess_number = ans_list[0]
            print(table["table"][-1])
            print(len(ans_list))

def main():
    runner = HitAndBlow()
    runner.run_first_half()
    runner.run_second_half()

if __name__ == "__main__":
    main()