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


@app.get('/get_cards/{user_id}')
async def get_cards(user_id: str, db: Session = Depends(get_db)):
    return crud.get_cards(db=db, user_id=int(user_id))


@app.get('/get_card_item', response_model=List[schemas.CardItem])
async def get_card(card_id: int, db: Session = Depends(get_db)):
    return crud.get_card(db=db, card_id=card_id)

