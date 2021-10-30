from datetime import datetime

from sqlalchemy.orm import registry
from sqlalchemy import exc
from sqlalchemy import (
    Column,
    DateTime,
)

from database import Session



mapper_reg = registry()
Base = mapper_reg.generate_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, nullable=True)

    def save(self, commit=True):
        session = Session()

        session.add(self)
        if commit:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def get_or_create(cls, commit=True, **kwargs):
        # if "url" not in kwargs:
        #     raise RuntimeError("url needed as unique value.")

        session = Session()
        try:
            return session \
                .query(cls) \
                .filter_by(**kwargs).one()
        except exc.NoResultFound as _:
            instance = cls(**kwargs)

            session.add(instance)
            if commit:
                try:
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise e
            return instance

    def update(self):
        Session().commit()