import enum

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    Boolean,
    String,
    Enum
)

from models.base import BaseModel



class OfferStatus(str, enum.Enum):
    CANCELED = "CANCELED"
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    TRANSFERRED = "TRANSFERRED"

class Offer(BaseModel):
    __tablename__ = "offer"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    prop_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)

    status = Column(Enum(OfferStatus), default=OfferStatus.PENDING)
    task_id = Column(String(length=128), nullable=True)

    accept_date = Column(DateTime, nullable=True)
    transfer_date = Column(DateTime, nullable=True)


    @property
    def canceled(self):
        return self.status == OfferStatus.CANCELED
