from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
import requests
import random

# 楽天API検索用
URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'
APP_ID = '1070572995802972997'
CARD_ITEM_NUM = 9

# ユーザー認証
def get_login_user(db: Session, user: schemas.User):
    login_user = db.query(models.User).filter(models.User.user_name == user.user_name).one_or_none()
    if login_user != None:
        return login_user
    else:
        raise HTTPException(status_code=404, detail="User not found.")

# ユーザー新規登録
def create_user(db: Session, user: schemas.User):
    registered = db.query(models.User) \
        .filter(models.User.user_name == user.user_name).all()
    print(len(registered))
    if len(registered)==0:
        db_user = models.User(
            user_name=user.user_name,
            finished_num=0
            )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="This username is already registered.")


# カード作成
def create_card(db: Session, user_id: int , sequence_num: int, books_genre_id: str):
    db_card = models.Card(
        user_id = user_id,
        sequence_num = sequence_num,
        is_finished = False
        )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    # 今追加したレコードのid
    card_id = db.query(models.Card).count() - 1
    create_card_items(db=db, card_id=card_id, books_genre_id=books_genre_id)


# カードアイテム作成
def create_card_items(db: Session, card_id: int , books_genre_id: str):
    params = {
        'applicationId': APP_ID,
        'books_genre_id': books_genre_id,
    }
    res = requests.get(URL, params)
    books = res.json()['Items']
    card_items = random.sample(books, CARD_ITEM_NUM)
    for i in range(CARD_ITEM_NUM):
        title = card_items[i]['Item']['title']
        item_url = card_items[i]['Item']['itemUrl']
        image_url = card_items[i]['Item']['largeImageUrl']
        db_card_item = models.CardItem(
            card_id = card_id,
            title = title,
            item_url = item_url,
            image_url = image_url,
            is_finished = False,
        )
        db.add(db_card_item)
        db.commit()
        db.refresh(db_card_item)

# ユーザーの全てのカードを取得
def get_cards(db: Session, user_id: int):
    card = db.query(models.Card) \
        .filter(models.Card.user_id == user_id) \
        .filter(models.Card.is_finished == False) \
        .all()
    return card

# カード1枚を取得
def get_card(db: Session, card_id: int):
    card = db.query(models.Card) \
        .filter(models.Card.card_id == card_id).one()
    return card

# カードの内容を取得
def get_card_items(db: Session, card_id: int):
    card_items = db.query(models.CardItem).filter(models.CardItem.card_id == card_id).all()
    return card_items


# 指定したカードを削除
def delete_card(db: Session, card_id: int):
    db_card = db.query(models.Card).filter(models.Card.card_id == card_id).one()
    db.delete(db_card)
    db.commit()
    db.refresh(db_card)