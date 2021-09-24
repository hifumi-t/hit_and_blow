import requests
URL = "https://damp-earth-70561.herokuapp.com"
session = requests.Session()
players = {"C":"290d6313-c662-45b6-82d6-6afb631ade08", "C2":"3cd613ef-a0c0-447c-bc23-81dcf1648be9"}

# すべての対戦部屋情報の取得
def get_all_room(URL=URL, session=session):
    url_get_all_room = URL + "/rooms"
    result = session.get(url_get_all_room)
    print(result.status_code)
    print(result.json())

# 指定した対戦部屋情報の取得
def get_room(room_id:int, URL=URL, session=session):
    url_get_room = URL + "/rooms/" + str(room_id)
    result = session.get(url_get_room)
    print(result.status_code)
    print(result.json())

# 対戦部屋へユーザーを登録
def enter_room(room_id:int, player, URL=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_enter_room = URL + "/rooms"
    post_data = {
        "player_id": players[player],
        "room_id": room_id
    }
    result_post = session.post(url_enter_room, headers=headers, json=post_data)
    print(result_post.status_code)
    print(result_post.json())

# 対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する
def get_table(room_id:int, player, URL=URL, session=session):
    url_get_table = URL + "/rooms/" + str(room_id) + "/players/" + player + "/table"
    result = session.get(url_get_table)
    print(result.status_code)
    print(result.json())

# 相手が当てる5桁の16進数を登録する
def post_hidden(room_id:int, player:str, URL=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_get_table = URL + "/rooms/" + str(room_id) + "/players/" + player + "/hidden"
    post_data = {
        "player_id": players[player],
        "hidden_number": "12345" # <--改良したい
    }
    result_post = session.post(url_get_table, headers=headers, json=post_data)
    print(result_post.status_code)
    print(result_post.json())

# 推測した数字を登録する
def post_guess(room_id:int, player:str, URL=URL, session=session):
    headers = {"Content-Type" : "application/json"}
    url_post_guess = URL + "/rooms/" + str(room_id) + "/players/" + player + "/table/guesses"
    post_data = {
        "player_id": players[player],
        "guess": "12345" # <--改良したい
    }
    result_post = session.post(url_post_guess, headers=headers, json=post_data)
    print(result_post.status_code)
    print(result_post.json())

# get_room(101)
# enter_room(102,"C")
# enter_room(102,"C2")
# post_hidden(102,"C")
# post_hidden(102,"C2")
# get_table(102,"C")
# post_guess(102,"C2")