import pytest
from fastapi import HTTPException

from src.main.models.messenger import User, Message


def test_user_create():
    user = User(username="chimbersaw")


@pytest.mark.xfail(raises=HTTPException, strict=True)
def test_user_empty():
    user = User(username="")


@pytest.mark.xfail(raises=HTTPException, strict=True)
def test_user_long_name():
    user = User(username="a" * (User.MAX_USERNAME_SIZE + 1))


def test_message_create():
    msg = Message(text="hi", sender="u1", recipient="u1")


@pytest.mark.xfail(raises=HTTPException, strict=True)
@pytest.mark.parametrize("text,sender,recipient", [("", "u1", "u2"), ("a", "", "u2"), ("a", "u1", "")])
def test_message_empty(text, sender, recipient):
    msg = Message(text=text, sender=sender, recipient=recipient)


@pytest.mark.xfail(raises=HTTPException, strict=True)
@pytest.mark.parametrize("text,sender,recipient", [
    ("x" * (Message.MAX_TEXT_SIZE + 1), "u1", "u2"),
    ("a", "x" * (User.MAX_USERNAME_SIZE + 1), "u2"),
    ("a", "u1", "x" * (User.MAX_USERNAME_SIZE + 1))
])
def test_message_long(text, sender, recipient):
    msg = Message(text=text, sender=sender, recipient=recipient)
