from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main.app import app
from src.main.db.database import Base, get_database
from src.main.db.models import UserDB
from src.main.models.messenger import Message, User
from src.main.routers.api import add_user, get_messages, send_message

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_database] = override_get_db


@pytest.fixture(autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_add_users():
    with TestingSessionLocal() as db:
        add_user(User(username="chimbersaw"), db)
        add_user(User(username="maslorij"), db)
        assert list(map(lambda u: u.username, db.query(UserDB).all())) == ["chimbersaw", "maslorij"]


def test_send_message():
    with TestingSessionLocal() as db:
        add_user(User(username="chimbersaw"), db)
        add_user(User(username="maslorij"), db)
        assert send_message(Message(text="hi", sender="chimbersaw", recipient="maslorij"), db).status_code == 200


@pytest.mark.xfail(raises=HTTPException, strict=True)
@pytest.mark.parametrize("text,sender,recipient", [
    ("hi", "1", "maslorij"),
    ("hi", "chimbersaw", "2"),
    ("", "chimbersaw", "maslorij"),
    ("hi", "", "maslorij"),
    ("hi", "chimbersaw", "")
])
def test_send_message_fail(text, sender, recipient):
    with TestingSessionLocal() as db:
        add_user(User(username="chimbersaw"), db)
        add_user(User(username="maslorij"), db)
        assert send_message(Message(text=text, sender=sender, recipient=recipient), db).status_code == 400


def test_get_messages():
    with TestingSessionLocal() as db:
        add_user(User(username="chimbersaw"), db)
        add_user(User(username="maslorij"), db)
        msg1 = Message(text="hi", sender="chimbersaw", recipient="maslorij")
        msg2 = Message(text="maslorij", sender="chimbersaw", recipient="maslorij")
        msg3 = Message(text="hello", sender="maslorij", recipient="chimbersaw")
        assert get_messages("chimbersaw", db) == []
        assert get_messages("maslorij", db) == []
        assert send_message(msg1, db).status_code == 200
        assert send_message(msg2, db).status_code == 200
        assert send_message(msg3, db).status_code == 200

        def create_message(m):
            return Message(text=m.text, sender=m.sender, recipient=m.recipient)

        assert list(map(create_message, get_messages("chimbersaw", db))) == [msg3]
        assert list(map(create_message, get_messages("maslorij", db))) == [msg1, msg2]


client = TestClient(app)


def test_request():
    assert client.post("/api/user/add", json={"username": "chimbersaw"}).status_code == 200
    assert client.post("/api/user/add", json={"username": "maslorij"}).status_code == 200
    assert client.post("/api/message/send", json={
        "text": "hi",
        "sender": "chimbersaw",
        "recipient": "maslorij"
    }).status_code == 200
    assert client.post("/api/message/send", json={
        "text": "!!!",
        "sender": "chimbersaw",
        "recipient": "maslorij"
    }).status_code == 200

    response = client.get("/api/message/maslorij")
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2
    for i in range(1):
        assert messages[i]["sender"] == "chimbersaw"
        assert messages[i]["recipient"] == "maslorij"
    assert messages[0]["text"] == "hi"
    assert messages[1]["text"] == "!!!"
