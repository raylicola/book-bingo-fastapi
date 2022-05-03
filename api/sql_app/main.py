from typing import List
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

@app.get('/get_cards/{user_id}', response_model=List[schemas.Card])
async def get_cards(user_id: str, db: Session = Depends(get_db)):
    return crud.get_cards(db=db, user_id=int(user_id))

@app.get('/get_card/{card_id}', response_model=schemas.Card)
async def get_card(card_id: str, db: Session = Depends(get_db)):
    return crud.get_cards(db=db, card_id=int(card_id))

@app.get('/get_card_item/{card_id}', response_model=List[schemas.CardItem])
async def get_card(card_id: int, db: Session = Depends(get_db)):
    return crud.get_card(db=db, card_id=card_id)

@app.post('/create_card/{user_id}/{selected_card}/?genre_id={}{', response_model=schemas.Card)
async def create_card(user_id: str, selected_card: str, genre_id: str, db: Session = Depends(get_db)):
    return create_card(db=db, user_id=int(user_id), selected_card=int(selected_card), booksGenreId=genre_id)