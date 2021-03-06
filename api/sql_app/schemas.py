from pydantic import BaseModel, Field

# ユーザー
class UserCreate(BaseModel):
    user_name: str = Field()

class User(UserCreate):
    user_id: int
    finished_num: int
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    user_id: int
class CardCreate(BaseModel):
    user_id: int
    sequence_num: int
    genre_id: str

class CardDelete(BaseModel):
    card_id: int

class CardUpdate(BaseModel):
    card_id: int
class Card(CardCreate):
    card_id: int
    is_finished: bool
    class Config:
        orm_mode = True

class CardItemUpdate(BaseModel):
    card_item_id: int
class CardItemCreate(BaseModel):
    card_id: int
    title: str
    item_url: str
    image_url: str
    is_finished: bool

class CardItem(CardItemCreate):
    card_item_id: int
    class Config:
        orm_mode = True