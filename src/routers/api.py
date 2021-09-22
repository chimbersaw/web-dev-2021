from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.models.item import Item

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello world!"


@router.get("/api/hello", response_class=PlainTextResponse)
def say_hello(username: str = "world"):
    return "Hello {}!".format(username)


@router.post("/api/items/")
def update_item(item: Item):
    return Item(
        username=item.username,
        price=item.price * 0.8,
        item_name=item.item_name + " (with discount)"
    )
