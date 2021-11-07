from decimal import Decimal

from pydantic import BaseModel



class PropBase(BaseModel):
    price: Decimal
    user_id: int


class PropCreate(PropBase):
    pass


class PropUpdate(PropBase):
    id: int


class Prop(PropBase):
    id: int

    class Config:
        orm_mode = True