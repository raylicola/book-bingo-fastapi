from urllib import response
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

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
