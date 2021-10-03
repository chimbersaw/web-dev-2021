import graphene
from datetime import datetime
from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
from src.main.models.messenger import User, Message, HelloQuery, EventsFromDateQuery, Event, MetaData
from src.main.db.mock_database import users, messages_received, events
from starlette.graphql import GraphQLApp

router = APIRouter()

router.add_route("/api/hello", GraphQLApp(schema=graphene.Schema(query=HelloQuery)))
router.add_route("/api/get_messages", GraphQLApp(schema=graphene.Schema(query=EventsFromDateQuery)))


@router.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello world!"


@router.post("/api/user/add")
def add_user(user: User):
    name = user.username
    if name in users:
        return PlainTextResponse(status_code=400, content="User already exists.")
    users.append(name)
    messages_received[name] = []
    return Response(status_code=200)


@router.get("/api/message/get/{username}", response_model=list[Message])
def get_messages(username: str):
    if username not in users:
        return PlainTextResponse(status_code=400, content="No user with username {}.".format(username))
    return messages_received[username]


@router.post("/api/message/send")
def send_message(message: Message):
    messages_received[message.recipient].append(message)
    events.append(Event(
        text=message.text,
        sender=message.sender,
        recipient=message.recipient,
        metadata=MetaData(time=datetime.now(), type="text"))
    )
    return Response(status_code=200)
