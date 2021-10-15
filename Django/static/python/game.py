import itertools
import random
from typing import List, Tuple, Union
from browser import document, html, ajax, timer
import json
class HitAndBlow:

    def __init__(self, i_am="C", strength=100) -> None:
        self.URL = "https://damp-earth-70561.herokuapp.com"
        #self.session = requests.Session()
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

    def get_all_room(self):
        import json
        """すべての対戦部屋情報の取得

        :rtype: dict
        :return: すべての対戦部屋情報
        """
        url_get_all_room = self.URL + "/rooms"
        req = ajax.Ajax()
        req.open('GET', url_get_all_room, False)   #False
        req.send()
        response = json.loads(req.responseText)
        #document['result'].text = response
        return(response)

    def get_valid_room_id(self):
        """入れる部屋（Cチーム用の中で一番若い数）

        :rtype: int
        :return: Cチーム用のIDの中で一番若い部屋ID
        """
        room_list_used = [i["id"] for i in self.result if i["id"]>=3000 and i["id"]<=3999]
        room_list = [i for i in range(3000,4000) if i not in room_list_used ]
        valid_id = room_list[0]
        return valid_id

    def enter_room(self) -> None:
        """対戦部屋へユーザーを登録
        :rtype: None
        :return: なし
        """
        #headers = {"Content-Type" : "application/json"}
        url_enter_room = self.URL + "/rooms"
        post_data = {
            "player_id": self.players[self.i_am],
            "room_id": self.room_id
            }
        post_data = json.dumps(post_data)
        req = ajax.Ajax()
        req.open('POST', url_enter_room, False)     
        req.set_header("Content-Type", "application/json")
        req.send(post_data)
        #document["result"].text = req.text

    def input_hidden_ply(self) -> str:
        """相手が当てる数字を登録する

        :rtype: str
        :return: 相手が当てる数字
        """
        self.hidden_number = document["hidden_num"].value
        return self.hidden_number

    def post_hidden_ply(self) -> str:
        """相手が当てる数字をサーバーに送る

        :rtype: str
        :return: 相手が当てる数字
        """
        #headers = {"Content-Type" : "application/json"}
        url_get_table = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/hidden"
        while True:
            self.hidden_number = self.input_hidden_ply()
            post_data = {
                "player_id": self.players[self.i_am],
                "hidden_number": self.hidden_number,
            }
            post_data = json.dumps(post_data)
            req = ajax.Ajax()
            req.open('POST', url_get_table, False)      
            req.set_header("Content-Type", "application/json")
            req.send(post_data)
            #document["result"].text = req.status
            if req.status == 200:
                return(self.hidden_number)
            else:
                #document["result"].text = "数字の重複は避けてください"
                break
                #リダイレクト

    def input_hidden_com(self) -> str:
        """相手が当てる数字を登録する

        :rtype: str
        :return: 相手が当てる数字
        """
        hidden = random.sample(self.num_list, 5)
        self.hidden_number = hidden[0]+hidden[1]+hidden[2]+hidden[3]+hidden[4]
        return self.hidden_number

    def post_hidden_com(self) -> str:
        """相手が当てる数字をサーバーに送る

        :rtype: str
        :return: 相手が当てる数字
        """
        #headers = {"Content-Type" : "application/json"}
        url_get_table = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/hidden"
        self.hidden_number = self.input_hidden_com()
        post_data = {
            "player_id": self.players[self.i_am],
            "hidden_number": self.hidden_number,
        }
        post_data = json.dumps(post_data)
        req = ajax.Ajax()
        req.set_header("Content-Type", "application/json")
        req.open('POST', url_get_table, False)
        req.send(post_data)
        return(self.hidden_number)

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
        import json
        url_get_table =  self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/table"
        req = ajax.Ajax()
        req.open('GET', url_get_table, False)
        req.send()
        response = json.loads(req.responseText)
        return(response)

    def check_win(self) -> bool:
        """勝敗が決まったかチェック

        :rtype: bool
        :return: 試合が続くならTrue
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
            document["result"].text = "YOU WIN"
        elif self.table_result["winner"] == None:
            document["result"].text = "DRAW"
        else:
            document["result"].text = "YOU LOSE"

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
        from .ans_list import Ans
        new_ans_list = []
        length = len(Ans)
        for self.ans in Ans[:length+1]:
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

    def post_guess_ply(self) -> None:
        """推測した数字を登録する

        :rtype: None
        :return: なし
        """
        #headers = {"Content-Type" : "application/json"}
        url_post_guess = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/table/guesses"
        post_data = {
            "player_id": self.players[self.i_am],
            "guess": document["guess"].value
        }
        post_data = json.dumps(post_data)
        req = ajax.Ajax()
        req.open('POST', url_post_guess, False) 
        req.bind("complete", self.on_complete)
        req.set_header("Content-Type", "application/json")
        req.send(post_data)

    def on_complete(self, req):
        if req.status == 200:
            table_result = self.get_table()
            r = list(table_result["table"][-1].values())
            r_str = "guess: " + str(r[0]) + ", hit: " + str(r[1]) + ", blow: " + str(r[2])
            document["table"] <= html.P(r_str)
            return(self.hidden_number)
        else:
            print("無効")

    def post_guess_com(self) -> None:
        """推測した数字を登録する

        :rtype: None
        :return: なし
        """
        #headers = {"Content-Type" : "application/json"}
        url_post_guess = self.URL + "/rooms/" + str(self.room_id) + "/players/" + self.i_am + "/table/guesses"
        post_data = {"player_id": self.players[self.i_am],"guess": self.guess_number}
        post_data = json.dumps(post_data)
        req = ajax.Ajax()
        req.open('POST', url_post_guess, True)
        req.set_header("Content-Type", "application/json")
        req.send(post_data.json())

roomid=""
p_hidden_number=""
c_hidden_number =""

def run(event):
    global roomid, p_hidden_number, c_hidden_number
    """ゲーム実行
    :rtype: None
    :return: なし
    """
    ply = HitAndBlow(i_am="C")
    com = HitAndBlow(i_am="C2",strength=document["cpu_level"].value)
    ply.result = ply.get_all_room()
    ply.room_id = ply.get_valid_room_id()
    roomid = ply.room_id
    com.room_id = ply.room_id
    ply.enter_room()
    com.enter_room()
    p_hidden_number = ply.post_hidden_ply()
    c_hidden_number = com.post_hidden_com()
    document["result"].text = "your turn"
    #document["turn"] <= html.H3("Your turn") 


def guess(event):
    global roomid,  p_hidden_number, c_hidden_number
    ply = HitAndBlow(i_am="C")
    com = HitAndBlow(i_am="C2", strength=document["cpu_level"].value)
    ply.hidden_number = p_hidden_number
    com.hidden_number = c_hidden_number
    com.room_id = roomid
    ply.room_id = roomid
    ply.table_result = ply.get_table()
    if ply.check_win() == False:    # 勝敗が決まっていたら, ゲーム終了
        ply.end_game()
    else:
        if ply.table_result["now_player"] == "C":   #自分のターンなら, 
            ply.post_guess_ply()
        else:
            # com.post_guess_com()
            # table, result = com.get_result()
            # com.ans_list = com.narrow_ans_list()
            # com.guess_number = com.ans_list[0]
            # document["record"] <= html.LI(table["table"][-1])
            pass




    # turn=True
    # while True: # ループ
    #     ply.table_result = ply.get_table()
    #     if ply.check_win() == False:    # 勝敗が決まっていたら, ゲーム終了
    #         ply.end_game()
    #         break
    #     else:
    #         if turn == True:   #自分のターンなら, 
    #             document["turn"] <= html.H4("Your turn")          
    #             while len(document["guess"].value) == 0:    
    #                 pass
    #             else:                           # guessの値が入ったら
    #                 ply.post_guess_ply()
    #                 document["guess"].clear()
    #                 turn = False
    #                 #document["guess"].value = "27654"
    #         else:
    #             # com.post_guess_com()
    #             # table, result = com.get_result()
    #             # com.ans_list = com.narrow_ans_list()
    #             # com.guess_number = com.ans_list[0]
    #             # document["record"] <= html.LI(table["table"][-1])
    #             turn = True
    #             break

def insert(event):
    record = document["record"]
    code = document["code"]
    if len(code.value) != 5:
        code.value = "5 digit only"

    elif len(code.value) != len(set(code.value)):
        code.value = "No duplication"

    else:
        record <= html.LI(code.value)
        code.value = ""

def nothing():
    pass

def ur_turn():
    document["code"].value = "Your turn"

def clear():
    document["code"].value = ""

def think():
    document["code"].value = "Let's think"

def Turn(turn):
    turn=False
    return turn

def zip(com):
    # document["guess"].value = "17654"
    document["table"] <= html.H3(com.hidden_number)

def post_wait(ply):
        #document["result"].text = len(document["guess"].value)
        if len(document["guess"].value) != 0:
            ply.post_guess_ply()
            ply.table_result = ply.get_table()
            document["result"].text = ply.table_result["table"][-1]
            # document["guess"].value = None
            # timer.set_timeout(Turn(turn), 5000)
        else:
            # continue
            document["guess"].value = "27654"

def flag(flag):
    flag = True
    return(flag)

def main():
    # document["check"].bind("click", check)
    # document["send"].bind("click", insert)
    document["game_start"].bind("click", run())
    document["send"].bind("click", guess())
    #run(ply, com)

if __name__ == "__main__":
    main()