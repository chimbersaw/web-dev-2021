from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import PlainTextResponse
from src.main.models.messenger import User, Message
from sqlalchemy.orm import Session
from src.main.db import database
from src.main.db import crud
from typing import List

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello world!"


@router.get("/api/hello", response_class=PlainTextResponse)
def say_hello(username: str = "world"):
    return "Hello {}!".format(username)


@router.post("/api/user/add")
def add_user(user: User, db: Session = Depends(database.get_database)):
    if not crud.add_user(db, user):
        return PlainTextResponse(status_code=400, content="User already exists.")
    return Response(status_code=200)


@router.post("/api/message/send")
def send_message(message: Message, db: Session = Depends(database.get_database)):
    if not crud.user_exists(db, message.sender):
        raise HTTPException(status_code=400, detail="Sender user does not exist.")
    if not crud.user_exists(db, message.recipient):
        raise HTTPException(status_code=400, detail="Recipient user does not exist.")
    crud.send_message(db, message)
    return Response(status_code=200)


@router.get("/api/message/{username}", response_model=List[Message])
def get_messages(username: str, db: Session = Depends(database.get_database)):
    if not crud.user_exists(db, username):
        return PlainTextResponse(status_code=400, content="No user with username {}.".format(username))
    return crud.get_messages(db, username)
