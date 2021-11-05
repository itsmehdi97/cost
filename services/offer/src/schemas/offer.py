from decimal import Decimal
from typing import Optional
from datetime import datetime


from pydantic import BaseModel

import models



class OfferBase(BaseModel):
    prop_id: int
    price: Decimal


class OfferCreate(OfferBase):
    user_id: int


class OfferUpdate(OfferBase):
    id: int
    status: Optional[models.OfferStatus]

class Offer(OfferBase):
    id: int
    user_id: int
    accept_date: Optional[datetime] = None
    transfer_date: Optional[datetime] = None
    status: Optional[models.OfferStatus]
    task_id: Optional[str]


    class Config:
        orm_mode = True