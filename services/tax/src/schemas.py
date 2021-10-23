from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.sql.sqltypes import DECIMAL

from pydantic import BaseModel



class PropertyBase(BaseModel):
    price: Decimal
    user_id: int


class PropertyCreate(PropertyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class PropertyUpdate(PropertyBase):
    id: int
    updated_at: datetime
    created_at: datetime
    transfer_date: Optional[datetime]


class Property(PropertyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True



class PropertyTransfer(PropertyBase):
    id: int
    transfer_date: datetime


class UserPropUpdate(PropertyBase):
    prop_id: int
    transfer_date: Optional[datetime] = None


class User(BaseModel):
    id: int
    username: str
