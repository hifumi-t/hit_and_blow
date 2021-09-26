#streamlitをpipでインストール後、
# streamlit run sample-streamlit.pyで実行

import streamlit as st
import numpy as np
import pandas as pd
import requests
from typing import Any

st.title("HIT & BLOW")

URL = "https://damp-earth-70561.herokuapp.com"

def get_room(session: requests.Session, room_id: int) -> Any:
    """<room_id>のroom情報取得
    """
    url_get_room = URL + "/rooms/" + str(room_id)
    result = session.get(url_get_room)

    if result.status_code == requests.codes.ok:
        return result.json()

def make_room_table(get_room_result):
    get_room_result = pd.DataFrame(get_room_result,index=['i',])
    st.table(get_room_result)

def main() -> None:
    session = requests.Session()
    room_id = st.number_input("調べたいルームIDを入力してください", 1, 10000)
    is_pushed = st.button("Get Room Information")
    if is_pushed:
        get_room_result = get_room(session, room_id)
        # st.write(get_room_result)
        make_room_table(get_room_result)

    

if __name__ == "__main__":
    main()