from sqlalchemy.orm import Session

from src.main.models.messenger import User, Message
from src.main.db.models import UserDB, MessageDB


def user_exists(db: Session, username: str):
    return db.query(UserDB).filter(UserDB.username == username).count() > 0


def add_user(db: Session, user: User):
    if user_exists(db, user.username):
        return None
    userDB = UserDB(username=user.username)
    db.add(userDB)
    db.commit()
    db.refresh(userDB)
    return userDB


def send_message(db: Session, message: Message):
    messageDB = MessageDB(
        text=message.text,
        sender=message.sender,
        recipient=message.recipient
    )
    db.add(messageDB)
    db.commit()
    db.refresh(messageDB)
    return messageDB


def get_messages(db: Session, username: str):
    return db.query(MessageDB).filter(MessageDB.recipient == username).all()
