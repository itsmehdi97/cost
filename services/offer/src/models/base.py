from datetime import datetime

from sqlalchemy.orm import registry
from sqlalchemy import exc
from sqlalchemy import (
    Column,
    DateTime,
)



mapper_reg = registry()
Base = mapper_reg.generate_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, nullable=True)
