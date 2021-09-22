from fastapi import HTTPException
from pydantic import BaseModel, validator


class Item(BaseModel):
    username: str
    price: float
    item_name: str

    @validator('price')
    def price_must_not_be_negative(cls, v):
        if v < 0:
            raise HTTPException(status_code=400, detail="Item price cannot be negative.")
        return v
