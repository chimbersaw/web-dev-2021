from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from src.models.item import Item

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello world!"


@app.get("/api/hello", response_class=PlainTextResponse)
def say_hello(username: str = "world"):
    return "Hello {}!".format(username)


@app.post("/api/items/")
def update_item(item: Item):
    return Item(
        username=item.username,
        price=item.price * 0.8,
        item_name=item.item_name + " (with discount)"
    )
