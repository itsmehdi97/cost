from decimal import Decimal
from typing import Optional

from sqlalchemy.sql.sqltypes import DECIMAL

from pydantic import BaseModel



class PropertyBase(BaseModel):
    title: str


class PropertyCreate(PropertyBase):
    user_id: Optional[int]
    title: str
    price: Decimal


class PropertyUpdate(PropertyBase):
    id: str
    title: str
    price: Decimal


class Property(PropertyBase):
    id: int
    user_id: int
    title: str
    price: Decimal

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
