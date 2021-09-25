# モジュールインポート，URL，プレイヤー情報の辞書登録
import requests
import sys
URL = "https://damp-earth-70561.herokuapp.com"
session = requests.Session()
players = {"C":"290d6313-c662-45b6-82d6-6afb631ade08", 
        "C2":"3cd613ef-a0c0-447c-bc23-81dcf1648be9"}
i_am = "C"

# 指定した対戦部屋情報の取得
def get_room(room_id:int, URL=URL, session=session):
    url_get_room = URL + "/rooms/" + str(room_id)
    result = session.get(url_get_room)
    return result.json()

# 対戦部屋へユーザーを登録
def enter_room(room_id:int, URL=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_enter_room = URL + "/rooms"
    post_data = {
        "player_id": players[i_am],
        "room_id": room_id
    }
    result_post = session.post(url_enter_room, headers=headers, json=post_data)
    print(result_post.json())

# 指定した対戦部屋の状況をチェック
def check_room():
    fin = ""
    while fin != "y":
        room_id_str = input("入室したい対戦部屋のIDを入力してください -->>")
        room_id = int(room_id_str)
        result = get_room(room_id)
        print(result)
        if result["state"] == -1:
            fin = input("部屋には誰もいません．入室しますか？[y/n] -->>")
        elif result["state"] == 1:
            fin = input("{}が待機しています．入室しますか？[y/n] -->>".format(result["player1"]))
        else:
            print("すでに部屋が満席です．別の部屋IDを入力してください")
    return room_id, result

# 相手に当てさせる番号をサーバーに送る
def post_hidden(room_id:int, URL=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_get_table = URL + "/rooms/" + str(room_id) + "/players/" + i_am + "/hidden"
    code = 0
    while code != 200:
        post_data = {
            "player_id": players[i_am],
            "hidden_number": input("相手に当てさせる番号を入力してください -->>")
        }
        result_post = session.post(url_get_table, headers=headers, json=post_data)
        code = result_post.status_code

# メンツがそろったか確認して相手に当てさせる番号を決める
def make_hidden(result, room_id):
    while result["state"] != 2:
        result = get_room(room_id)
    post_hidden(room_id)

# 対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する
def get_table(room_id:int, i_am, URL=URL, session=session):
    url_get_table = URL + "/rooms/" + str(room_id) + "/players/" + i_am + "/table"
    table_result = session.get(url_get_table)
    # print(table_result.status_code)
    # print(table_result.json())
    return table_result

# 勝敗が決まったかチェック
def check_win(table_result):
    if table_result["state"] == 2:
        return True # →ゲーム続行
    else:
        return False # →ゲーム終了

# 自分のターンかチェック
def check_turn(table_result):
    if table_result["now_player"] == i_am:
        return True # →自分のターン
    else:
        return False # →相手のターン

# ゲーム終了
def end_game(table_result):
    if table_result["winner"] == i_am:
        print("あなたの勝ちです！おめでとう！")
    elif table_result["winner"] == None:
        print("引き分けです")
    else:
        print("あなたの負けです...")

# 推測した数字を登録する
def post_guess(room_id:int, i_am, URL=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_post_guess = URL + "/rooms/" + str(room_id) + "/players/" + i_am + "/table/guesses"
    post_data = {
        "player_id": players[i_am],
        "guess": input("相手の番号を推測して入力してください -->>")
    }
    result_post = session.post(url_post_guess, headers=headers, json=post_data)
    # print(result_post.status_code)
    # print(result_post.json())

def main():
    room_id, result = check_room() #部屋番号を入れて空き状況を確認する．入室を決めた部屋の情報を返す．
    enter_room(room_id) #入室する
    make_hidden(result, room_id) #相手に当てさせる番号を決める．例外処理もOK

    while True:
        turn = False
        while turn != True:
            table_result = get_table(room_id, i_am)
            table_result = table_result.json()
            if check_win(table_result) == False:
                end_game(table_result)
                sys.exit()
            else:
                turn = check_turn(table_result)
        post_guess(room_id, i_am)
        table_result = get_table(room_id, i_am)
        print(table_result.json()["table"])

if __name__ == "__main__":
    main()