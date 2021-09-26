import pytest
from fastapi import HTTPException

from src.main.db.mock_database import *
from src.main.models.messenger import User, Message
from src.main.routers.api import add_user, send_message, get_messages


@pytest.fixture(autouse=True)
def add_users():
    clear_database()
    yield
    clear_database()


def test_add_users():
    add_user(User(username="chimbersaw"))
    add_user(User(username="maslorij"))
    assert users == ["chimbersaw", "maslorij"]


def test_send_message():
    add_user(User(username="chimbersaw"))
    add_user(User(username="maslorij"))
    assert send_message(Message(text="hi", sender="chimbersaw", recipient="maslorij")).status_code == 200


@pytest.mark.xfail(raises=HTTPException, strict=True)
@pytest.mark.parametrize("text,sender,recipient", [
    ("hi", "1", "maslorij"),
    ("hi", "chimbersaw", "2"),
    ("", "chimbersaw", "maslorij"),
    ("hi", "", "maslorij"),
    ("hi", "chimbersaw", "")
])
def test_send_message_fail(text, sender, recipient):
    add_user(User(username="chimbersaw"))
    add_user(User(username="maslorij"))
    assert send_message(Message(text=text, sender=sender, recipient=recipient)).status_code == 400


def test_get_messages():
    add_user(User(username="chimbersaw"))
    add_user(User(username="maslorij"))
    msg1 = Message(text="hi", sender="chimbersaw", recipient="maslorij")
    msg2 = Message(text="maslorij", sender="chimbersaw", recipient="maslorij")
    msg3 = Message(text="hello", sender="maslorij", recipient="chimbersaw")
    assert get_messages("chimbersaw") == []
    assert get_messages("maslorij") == []
    assert send_message(msg1).status_code == 200
    assert send_message(msg2).status_code == 200
    assert send_message(msg3).status_code == 200
    assert get_messages("chimbersaw") == [msg3]
    assert get_messages("maslorij") == [msg1, msg2]
