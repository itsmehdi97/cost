from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    Boolean
)

from models.base import BaseModel



class Offer(BaseModel):
    __tablename__ = "offer"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    prop_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)

    canceled = Column(Boolean, default=False)
    accepted = Column(Boolean, default=False)
    accept_date = Column(DateTime, nullable=True)
