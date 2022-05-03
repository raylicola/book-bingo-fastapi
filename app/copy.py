from tkinter import Image
import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image

MAX_CARD_NUM = 3
CARD_ITEM_NUM = 9

user_id = 1
user_name = 'Yamada'
finish_num = 0
get_cards_url = 'http://127.0.0.1:8000/get_cards/' + str(user_id)
res = requests.get(get_cards_url)
cards = res.json()
st.write(cards)

# key: sequence_num, value: card_id
card_dict = {}
if len(card_dict) != 0:
    for i in range(MAX_CARD_NUM):
        card_dict[cards['sequence_num']] = cards['card_id']

# key: sequence_num, valur: カードが存在するか否か
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
        card_delete_url = 'http://127.0.0.1:8000/delete_card/' + str(card_id)
        card_state_dict[sequence_num] == False
else:
    selected_genre = st.sidebar.selectbox(
        'ジャンルを選択してください',
        (
            '小説・エッセイ', 'ビジネス・経済・就職', '旅行・留学・アウトドア',
            '人文・思想・社会', 'ホビー・スポーツ・美術', '美容・暮らし・健康',
            '科学・技術', '文庫', '新書',
        ))
    genre_id_mapping = {
        '小説・エッセイ': '0010',
        'ビジネス・経済・就職': '0010',
        '旅行v留学・アウトドア': '0010',
        '人文・思想・社会': '0010',
        'ホビー・スポーツ・美術': '0010',
        '美容・暮らし・健康': '0010',
        '科学・技術': '0010',
        '文庫': '0010',
        '新書': '0010',
    }
    genre_id = genre_id_mapping[selected_genre]
    if st.sidebar.button('カードを作成'):
        card_create_url = 'http://127.0.0.1:8000/create_card/' + str(user_id) + '/' + str(sequence_num) + '/?books_genre_id=' + genre_id
        card_state_dict[sequence_num] == True


# ビンゴカード
for i in range(MAX_CARD_NUM):
    if card_state_dict[sequence_num] == True:
        get_card_url = 'http://127.0.0.1:8000/get_card/' + str(card_dict[cards['sequence_num']])
        res = requests.get(get_card_url)
        card = res.json()
        st.write(cards)
        get_card_items_url = 'http://127.0.0.1:8000/get_card_items/' + str(card['card_id'])
        res = requests.get(get_card_items_url)
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