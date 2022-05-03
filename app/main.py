from tkinter import Image
import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image

MAX_CARD_NUM = 3
CARD_ITEM_NUM = 9
page = st.sidebar.selectbox('ページを選択してください', ['ログイン', 'ユーザー登録', 'ビンゴ'])

# ログイン済みかどうか判定
try:
    user_id = st.session_state.user_id
    user_name = st.session_state.user_name
    finish_num = st.session_state.finished_num
    if page in ['ログイン', 'ユーザー登録']:
        st.error('ログイン済みです')
    elif page == 'ビンゴ':
        get_card_url = 'http://127.0.0.1:8000/get_card/' + str(user_id)
        res = requests.get(get_card_url)
        # key: sequence_num, value: card_id
        cards = res.json()
        card_dict = {}
        for i in range(MAX_CARD_NUM):
            card_dict[cards['sequence_num']] = cards['card_id']

        card_state_dict = {}

        for i in range(MAX_CARD_NUM):
            if i in card_dict.keys():
                card_state_dict[i] = True
            else:
                card_state_dict[i] = False

        st.sidebar.title(user_name + 'さん')
        st.sidebar.title('BINGO達成：' + str(finish_num) + '枚')

        # ビンゴカードを選択（3枚まで登録可能）
        select_card = st.sidebar.radio(
            'ビンゴカードを選択',
            (1,2,3))

        if card_state_dict[select_card] == True:
            if st.sidebar.button('カードを削除'):
                card_delete_url = 'http://127.0.0.1:8000/delete_card/{card_id}'
                card_state_dict[select_card] == False
        else:
            if st.sidebar.button('カードを作成'):
                card_create_url = 'http://127.0.0.1:8000/create_card'
                card_state_dict[select_card] == True

        # ビンゴカード
        for i in range(MAX_CARD_NUM):
            if card_state_dict[select_card] == True:
                get_card_item_url = 'http://127.0.0.1:8000/get_card/' + str(card_dict[i])
                res = requests.get(get_card_item_url)
                card_items = res.json()
                for i in list(range(3)):
                    col= st.columns(3)
                    for j in list(range(3)):
                        with col[j]:
                            if st.checkbox(str(i*3+j+1)):
                                img = Image.open(f'api/img/translucent.jpeg')
                                st.image(img, use_column_width=True)
                            else:
                                title = card_items[i*3+j]['title']
                                item_url = card_items[i*3+j]['item_url']
                                image_url = card_items[i*3+j]['image_url']
                                is_finished = card_items[i*3+j]['is_finished']
                                st.markdown(f'[{title}]({item_url})', unsafe_allow_html=True)
                                img = Image.open(image_url)
                                st.image(img, use_column_width=True)

except:
    if page == 'ログイン':
        st.title('ログイン')
        with st.form(key='login'):
            user_name: str = st.text_input('ユーザー名')
            data = {
                'user_name': user_name
            }
            login_button = st.form_submit_button(label='ログイン')
        if login_button:
            login_url = 'http://127.0.0.1:8000/login'
            res = requests.post(
                login_url,
                data=json.dumps(data)
            )
            if res.status_code==200:
                st.success('ログイン完了')
                user_id = str(res.json()['user_id'])
                st.session_state.user_id = res.json()['user_id']
                st.session_state.user_name = res.json()['user_name']
                st.session_state.finished_num = res.json()['finished_num']
            elif res.status_code==404:
                st.error('ユーザーが見つかりません')

    elif page == 'ユーザー登録':
        st.title('ユーザー登録')
        with st.form(key='signup'):
            user_name: str = st.text_input('ユーザー名')
            data = {
                'user_name': user_name
            }
            signup_button = st.form_submit_button(label='登録')

        if signup_button:
            signup_url = 'http://127.0.0.1:8000/signup'
            res = requests.post(
                signup_url,
                data=json.dumps(data)
            )
            if res.status_code==200:
                st.success('ユーザー登録が完了しました。ログイン画面からログインしてください。')
                st.write(res.status_code)
            elif res.status_code==404:
                st.error('ユーザーは既に登録されています。')

    elif page == 'ビンゴ':
        st.error('ログインしてください')
