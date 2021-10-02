# モジュールインポート，URL，プレイヤー情報の辞書登録
import requests
from typing import Tuple

URL = "https://damp-earth-70561.herokuapp.com"
session = requests.Session()
players = {"C":"290d6313-c662-45b6-82d6-6afb631ade08", 
        "C2":"3cd613ef-a0c0-447c-bc23-81dcf1648be9"}
i_am = "C"

# 指定した対戦部屋情報の取得
def get_room(room_id:int, URL:str=URL, session=session) -> dict:
    url_get_room = URL + "/rooms/" + str(room_id)
    result = session.get(url_get_room)
    return result.json()

# 部屋IDの入力
def input_roomID():
    room_id_str = input("入室したい対戦部屋のIDを入力してください -->>")
    room_id = int(room_id_str)
    return room_id

# 部屋の情報を取得して，状況を返す
def check_room(room_id:int):
    get_room_result = get_room(room_id)
    if get_room_result["state"] == -1:
        print("部屋には誰もいません")
        return True
    elif get_room_result["state"] == 1:
        print("{}が待機しています".format(get_room_result["player1"]))
        return True
    else:
        print("すでに部屋が満席です．別の部屋IDを入力してください")
        return False

# 部屋に入室するか選択する
def ask_enter_room():
    while True:
        ans = input("入室しますか？[y/n] -->>")
        if ans == "y":
            return True
        elif ans == "n":
            return False
        else:
            print("y/n以外の入力がされました．入力をやり直してください")

# 対戦部屋へユーザーを登録
def enter_room(room_id:int, i_am:str=i_am, URL:str=URL, session=session) -> None:
    headers = {"Content-Type" : "application/json"}
    url_enter_room = URL + "/rooms"
    post_data = {
        "player_id": players[i_am],
        "room_id": room_id
        }
    result_post = session.post(url_enter_room, headers=headers, json=post_data)
    print(result_post.json())

def input_hidden() -> str:
    hidden_number = input("相手に当てさせる番号を入力してください -->>")
    return hidden_number

# 相手に当てさせる番号をサーバーに送る
def post_hidden(room_id:int, i_am:str=i_am, URL:str=URL, session=session) -> str:
    headers = {"Content-Type" : "application/json"}
    url_get_table = URL + "/rooms/" + str(room_id) + "/players/" + i_am + "/hidden"
    
    while True:
        hidden_number = input_hidden()
        post_data = {
            "player_id": players[i_am],
            "hidden_number": hidden_number
        }
        result_post = session.post(url_get_table, headers=headers, json=post_data)
        if result_post.status_code == 200:
            print(f"{hidden_number}を相手に当ててもらいます")
            return hidden_number
        else:
            print("無効な入力がされました")

def run_first_half() -> Tuple[int, str]:
    """プログラム前半（ID入力から相手が当てる数字を入力まで）

    :rtype: Tuple[int, str]
    :return: 入室したルームID，相手が当てる数字
    """
    enter = ""
    while enter != True: # 部屋に入るまで繰り返す
        room = ""
        while room != True: # 入れる部屋を選ぶまで繰り返す
            room_id = input_roomID()
            room = check_room(room_id)
        enter = ask_enter_room()
    enter_room(room_id)
    get_room_result = get_room(room_id)
    while get_room_result["state"] != 2:
        get_room_result = get_room(room_id)
    hidden_number = post_hidden(room_id)
    return room_id, hidden_number

# 対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する
def get_table(room_id:int, i_am:str=i_am, URL:str=URL, session=session) -> dict:
    url_get_table = URL + "/rooms/" + str(room_id) + "/players/" + i_am + "/table"
    table_result = session.get(url_get_table)
    return table_result.json()

# 勝敗が決まったかチェック
def check_win(table_result:dict) -> bool:
    if table_result["state"] == 2:
        return True # →ゲーム続行
    else:
        return False # →ゲーム終了

# 自分のターンかチェック
def check_turn(table_result, i_am:str=i_am) -> bool:
    if table_result["now_player"] == i_am:
        return True # →自分のターン
    else:
        return False # →相手のターン

# ゲーム終了
def end_game(table_result, i_am:str=i_am):
    if table_result["winner"] == i_am:
        print("あなたの勝ちです！おめでとう！")
    elif table_result["winner"] == None:
        print("引き分けです")
    else:
        print("あなたの負けです...")

# 推測した数字を登録する
def post_guess(room_id:int, i_am:str=i_am, URL:str=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_post_guess = URL + "/rooms/" + str(room_id) + "/players/" + i_am + "/table/guesses"
    post_data = {
        "player_id": players[i_am],
        "guess": input("相手の番号を推測して入力してください -->>") # <<-- 推測アルゴリズムの出力先
    }
    result_post = session.post(url_post_guess, headers=headers, json=post_data)

def run_second_half(room_id):
    while True:
        turn = False
        while turn != True:
            table_result = get_table(room_id)
            if check_win(table_result) == False:
                end_game(table_result)
                return
            else:
                turn = check_turn(table_result)
        post_guess(room_id)
        table_result = get_table(room_id)
        print(table_result["table"])

def main():
    room_id, hidden_number = run_first_half()
    run_second_half(room_id)

if __name__ == "__main__":
    main()