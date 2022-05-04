from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from .database import Base


# ユーザー
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    finished_num = Column(Integer)


# ビンゴカード
class Card(Base):
    __tablename__ = "cards"
    card_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    sequence_num = Column(Integer)   # 1..3
    is_finished = Column(Boolean)


# カードに書かれたアイテム
class CardItem(Base):
    __tablename__ = "card_items"
    card_item_id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.card_id", ondelete="CASCADE"), nullable=False)
    title = Column(String)
    item_url = Column(String)
    image_url = Column(String)
    is_finished = Column(Boolean)