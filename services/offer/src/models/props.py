from sqlalchemy import (
    Column,
    Integer,
    Numeric
)

from models.base import BaseModel



class Prop(BaseModel):
    __tablename__ = "prop"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)