from typing import List
from urllib import response
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .import crud, models, schemas
from .database import engine, SessionLocal

# DB作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DBのセッション獲得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/login', response_model=schemas.User)
async def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.get_login_user(db=db, user=user)

@app.post('/signup', response_model=schemas.User)
async def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post('/create_card', response_model=List[schemas.CardItem])
async def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    return crud.create_card(db=db, card=card)

@app.post('/update_user', response_model=schemas.User)
async def create_card(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user=user)

@app.post('/delete_card')
async def create_card(card: schemas.CardDelete, db: Session = Depends(get_db)):
    return crud.delete_card(db=db, card=card)

@app.post('/update_card')
async def update_card(card: schemas.CardUpdate, db: Session = Depends(get_db)):
    return crud.update_card(db=db, card=card)

@app.post('/update_card_item', response_model=schemas.CardItem)
async def update_card_item(card_item: schemas.CardItemUpdate, db: Session = Depends(get_db)):
    return crud.update_card_item(db=db, card_item=card_item)


@app.get('/get_cards/{user_id}')
async def get_cards(user_id: str, db: Session = Depends(get_db)):
    return crud.get_cards(db=db, user_id=int(user_id))


@app.get('/get_card_items/{card_id}', response_model=List[schemas.CardItem])
async def get_card_items(card_id: str, db: Session = Depends(get_db)):
    return crud.get_card_items(db=db, card_id=int(card_id))

