from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    username: str
    price: float
    item_name: str


@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello world!"


@app.get("/api/hello", response_class=PlainTextResponse)
def say_hello(username: str = "world"):
    return "Hello {}!".format(username)


@app.post("/api/items/")
def update_item(item: Item):
    if item.price < 0:
        raise HTTPException(status_code=400, detail="Item price cannot be negative.")

    return Item(
        username=item.username,
        price=item.price * 0.8,
        item_name=item.item_name + " (with discount)"
    )
