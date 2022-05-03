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
st.write(res)
cards = res.json()
st.write('cards')
st.json(cards)

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

# key: sequence_num, value: card_id
card_dict = {}
if len(card_dict) != 0:
    for i in range(MAX_CARD_NUM):
        card_dict[cards[i]['sequence_num']] = cards['card_id']

st.write('card_dict')
st.write(card_dict)

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
    card_id = card_dict['sequence_num']
    if st.sidebar.button('カードを削除'):
        card_delete_url = 'http://127.0.0.1:8000/delete_card/' + str(card_id)
        card_state_dict[sequence_num] == False
else:
    selected_genre = st.sidebar.selectbox(
        'ジャンルを選択してください',
        books_genre
        )
    genre_id = books_genre_id_mapping[selected_genre]
    if st.sidebar.button('カードを作成'):
        create_card = 'http://127.0.0.1:8000/create_card'
        data = {
            'user_id': user_id,
            'sequence_num': sequence_num,
            'genre_id': genre_id,
        }
        res = requests.post(
            create_card,
            data=json.dumps(data)
        )
        card_state_dict[sequence_num] == True


# ビンゴカード
for i in range(MAX_CARD_NUM):
    if card_state_dict[sequence_num] == True:
        get_card_items_url = 'http://127.0.0.1:8000/get_card_items'
        data = {
        }
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