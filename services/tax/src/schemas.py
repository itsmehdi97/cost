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
    created_at: datetime
    updated_at: Optional[datetime]


class Property(PropertyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
