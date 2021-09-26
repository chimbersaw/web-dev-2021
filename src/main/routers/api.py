from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
from src.main.models.messenger import User, Message
from src.main.db.mock_database import users, messages_received

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello world!"


@router.get("/api/hello", response_class=PlainTextResponse)
def say_hello(username: str = "world"):
    return "Hello {}!".format(username)


@router.post("/api/user/add")
def add_user(user: User):
    name = user.username
    if name in users:
        return PlainTextResponse(status_code=400, content="User already exists.")
    users.append(name)
    messages_received[name] = []
    return Response(status_code=200)


@router.get("/api/message/{username}", response_model=list[Message])
def get_messages(username: str):
    if username not in users:
        return PlainTextResponse(status_code=400, content="No user with username {}.".format(username))
    return messages_received[username]


@router.post("/api/message/send")
def send_message(message: Message):
    messages_received[message.recipient].append(message)
    return Response(status_code=200)
