import pytest

from src.main.db.mock_database import *


@pytest.fixture(autouse=True)
def add_users():
    clear_database()
    yield
    clear_database()


def test_users():
    assert len(users) == 0
    users.append("user1")
    users.append("user2")
    assert "user1" in users
    assert "user2" in users
    assert "user3" not in users
    assert len(users) == 2


def test_messages_received():
    assert len(messages_received) == 0
    messages_received["user1"] = ["msg1", "msg2"]
    messages_received["user2"] = []
    assert "msg1" in messages_received["user1"]
    assert "msg2" in messages_received["user1"]
    assert "msg3" not in messages_received["user1"]
    assert len(messages_received["user1"]) == 2
    assert len(messages_received["user2"]) == 0
    assert len(messages_received) == 2
