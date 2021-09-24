# モジュールインポート，URL，プレイヤー情報の辞書登録
import requests
URL = "https://damp-earth-70561.herokuapp.com"
session = requests.Session()
players = {"C":"290d6313-c662-45b6-82d6-6afb631ade08", "C2":"3cd613ef-a0c0-447c-bc23-81dcf1648be9"}
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
    while fin is not "y":
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
    while code is not 200:
        post_data = {
            "player_id": players[i_am],
            "hidden_number": input("相手に当てさせる番号を入力してください．")
        }
        result_post = session.post(url_get_table, headers=headers, json=post_data)
        code = result_post.status_code
        print(result_post.status_code)
    print(result_post.json())

# メンツがそろったか確認して相手に当てさせる番号を決める
def make_hidden(room_id, result):
    while result["state"] is not 2:
        result = get_room(room_id)
    post_hidden(room_id)





def main():
    room_id, result = check_room() #部屋番号を入れて空き状況を確認する．入室を決めた部屋の情報を返す．
    enter_room(room_id) #入室する
    make_hidden(room_id, result) #相手に当てさせる番号を決める．例外処理もOK

if __name__ == "__main__":
    main()