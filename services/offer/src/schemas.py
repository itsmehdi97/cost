from decimal import Decimal
from typing import Optional
from datetime import datetime


from pydantic import BaseModel



class OfferBase(BaseModel):
    prop_id: int
    price: int


class OfferCreate(OfferBase):
    user_id: int


class OfferUpdate(OfferBase):
    id: int
    canceled: Optional[bool] = False


class Offer(OfferBase):
    id: int
    user_id: int
    canceled: bool

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
