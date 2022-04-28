from enum import unique
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .database import Base

# class User(Base):
#     # テーブル名の定義
#     __tablename__ = "users"
#     user_id = Column(Integer, primary_key=True, index=True)