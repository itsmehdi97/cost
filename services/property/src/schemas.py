from decimal import Decimal
from typing import Optional
from datetime import datetime

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
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    id: int
    user_id: int
    title: str
    price: Decimal

    class Config:
        orm_mode = True


class PropertyTransfer(BaseModel):
    id: int
    price: Decimal
    user_id: int
    transfer_date: datetime


class User(BaseModel):
    id: int
    username: str
