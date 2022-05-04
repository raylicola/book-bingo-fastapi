# TODO:
# 商品検索で同じものばかり出てこないよう改善
# カード削除時にrefreshするとエラーが発生する
from calendar import c
from tkinter import Image
import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image

MAX_CARD_NUM = 3
CARD_ITEM_NUM = 9
APP_URL = 'http://127.0.0.1:8000/'

books_genre = (
        '小説・エッセイ', 'ビジネス・経済・就職', '旅行・留学・アウトドア',
        '人文・思想・社会', 'ホビー・スポーツ・美術', '美容・暮らし・健康',
        '科学・技術', '文庫', '新書',
)
books_genre_id_mapping = {
        '小説・エッセイ': '001004',
        'ビジネス・経済・就職': '001006',
        '旅行・留学・アウトドア': '001007',
        '人文・思想・社会': '001008',
        'ホビー・スポーツ・美術': '001009',
        '美容・暮らし・健康': '001010',
        '科学・技術': '001012',
        '文庫': '001019',
        '新書': '001020',
    }

bingo_combination = [
    [1,2,3],[4,5,6],[7,8,9],
    [1,4,7],[2,5,8],[3,6,9],
    [1,5,9],[3,5,7]
]
def judge_bingo(checked_cols):
    searched = [
        [1,2,3],[4,5,6],[7,8,9],
        [1,4,7],[2,5,8],[3,6,9],
        [1,5,9],[3,5,7]
    ]
    for index, bingo_list in enumerate(searched):
        for checked_num in checked_cols:
            if checked_num in bingo_list:
                bingo_list.remove(checked_num)
            if len(bingo_list)==0:
                return index


page = st.sidebar.selectbox('ページを選択してください', ['ログイン', 'ユーザー登録', 'ビンゴ'])

# ログイン済みかどうか判定
try:
    user_id = st.session_state.user_id
    user_name = st.session_state.user_name
    finish_num = st.session_state.finished_num
    if page in ['ログイン', 'ユーザー登録']:
        st.error('ログイン済みです')
    elif page == 'ビンゴ':
        get_cards_url = 'get_cards/' + str(user_id)
        res = requests.get(APP_URL+get_cards_url)
        # key: sequence_num, value: card_id
        cards = res.json()
        card_dict = {}
        for i in range(len(cards)):
            card_dict[cards[i]['sequence_num']] = cards[i]['card_id']

        card_state_dict = {}

        for i in range(1,MAX_CARD_NUM+1):
            if i in card_dict.keys():
                card_state_dict[i] = True
            else:
                card_state_dict[i] = False

        st.sidebar.title(user_name + 'さん')
        st.sidebar.title('BINGO達成：' + str(finish_num) + '枚')

        # ビンゴカードを選択（3枚まで登録可能）
        sequence_num = st.sidebar.radio(
            'ビンゴカードを選択',
            (1,2,3))

        if card_state_dict[sequence_num] == True:
            card_id = card_dict[sequence_num]
            if st.sidebar.button('カードを削除'):
                card_delete_url = 'delete_card'
                data = {
                'card_id': card_id,
                }
                res = requests.post(
                    APP_URL+card_delete_url,
                    data=json.dumps(data)
                )
                st.sidebar.write('カードを削除しました')
                card_state_dict[sequence_num] == False
        else:
            selected_genre = st.sidebar.selectbox(
                'ジャンルを選択してください',
                books_genre
                )
            genre_id = books_genre_id_mapping[selected_genre]
            if st.sidebar.button('カードを作成'):
                create_card_url = 'create_card'
                data = {
                    'user_id': user_id,
                    'sequence_num': sequence_num,
                    'genre_id': genre_id,
                }
                res = requests.post(
                    APP_URL+create_card_url,
                    data=json.dumps(data)
                )
                card_state_dict[sequence_num] == True
                st.success('カードを作成しました')

        # ビンゴカード
        for i in range(1,MAX_CARD_NUM+1):
            if (sequence_num == i) and (card_state_dict[sequence_num] == True):
                card_id = card_dict[i]
                get_card_items_url = 'get_card_items/' + str(card_id)
                res = requests.get(APP_URL+get_card_items_url)
                card_items = res.json()
                checked_cols = []
                for i in list(range(3)):
                    col= st.columns(3)
                    for j in list(range(3)):
                        with col[j]:
                            card_item_id = card_items[i*3+j]['card_item_id']
                            is_finished = card_items[i*3+j]['is_finished']
                            title = card_items[i*3+j]['title']
                            item_url = card_items[i*3+j]['item_url']
                            image_url = card_items[i*3+j]['image_url']
                            if is_finished==True:
                                checked_cols.append(i*3+j+1)
                            update_card_items_url = 'update_card_item'
                            # checkbox = st.checkbox(str(i*3+j+1), value=is_finished)
                            if is_finished == True:
                                checkbox = st.checkbox(str(i*3+j+1), value=True)
                                st.markdown(f'[{title}]({item_url})', unsafe_allow_html=True)
                                st.image(image_url, use_column_width=True)
                                if not checkbox:
                                    data = {
                                        'card_item_id': card_item_id
                                    }
                                    res = requests.post(
                                        APP_URL+update_card_items_url,
                                        data=json.dumps(data)
                                    )
                                    checked_cols.remove(i*3+j+1)

                            else:
                                checkbox = st.checkbox(str(i*3+j+1), value=False)
                                st.markdown(f'[{title}]({item_url})', unsafe_allow_html=True)
                                st.image(image_url, use_column_width=True)
                                if checkbox:
                                    data = {
                                        'card_item_id': card_item_id
                                    }
                                    res = requests.post(
                                        APP_URL+update_card_items_url,
                                        data=json.dumps(data)
                                    )
                                    checked_cols.append(i*3+j+1)

                if judge_bingo(checked_cols) != None:
                    if st.sidebar.button('ビンゴです！'):
                        delete_card_url = 'delete_card'
                        data = {
                            'card_id': card_id,
                        }
                        res = requests.post(
                            APP_URL+delete_card_url,
                            data=json.dumps(data)
                        )
                        update_user_url = 'update_user'
                        data = {
                            'user_id': user_id,
                        }
                        res = requests.post(
                            APP_URL+update_user_url,
                            data=json.dumps(data)
                        )
                        st.session_state.finished_num = res.json()['finished_num']
                        st.sidebar.write('カードを削除しました')
                        card_state_dict[sequence_num] == False

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
            login_url = 'login'
            res = requests.post(
                APP_URL+login_url,
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
            signup_url = 'signup'
            res = requests.post(
                APP_URL+signup_url,
                data=json.dumps(data)
            )
            if res.status_code==200:
                st.success('ユーザー登録が完了しました。ログイン画面からログインしてください。')
            elif res.status_code==404:
                st.error('ユーザーは既に登録されています。')
