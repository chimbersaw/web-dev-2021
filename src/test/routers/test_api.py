import pytest

from src.main.db.mock_database import clear_database
from src.main.routers.api import *


@pytest.fixture(autouse=True)
def add_users():
    clear_database()
    yield
    clear_database()


def test_read_root():
    assert read_root() == "Hello world!"


def text_say_hello():
    assert say_hello() == "Hello world!"


def text_say_hello_named():
    assert say_hello("chimbersaw") == "Hello chimbersaw!"


def test_add_user():
    user = User(username="chimbersaw")
    assert add_user(user).status_code == 200
    assert users == ["chimbersaw"]
    assert messages_received == {"chimbersaw": []}


def test_add_user_exists():
    user = User(username="chimbersaw")
    assert add_user(user).status_code == 200
    assert add_user(user).status_code == 400


def test_get_messages():
    user = User(username="chimbersaw")
    add_user(user)
    assert get_messages("chimbersaw") == []


def test_get_messages_not_exists():
    assert get_messages("chimbersaw").status_code == 400


@pytest.mark.xfail(strict=True)
def test_send_messages_fail():
    send_message(Message(text="a", sender="b", recipient="c"))
