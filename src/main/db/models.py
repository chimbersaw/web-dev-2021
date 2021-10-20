from sqlalchemy import Column, Integer, String

from src.main.db.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    sender = Column(String, index=True)
    recipient = Column(String, index=True)
