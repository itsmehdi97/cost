from abc import ABCMeta
from datetime import datetime

from sqlalchemy.orm import registry, relationship
from sqlalchemy import exc
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime
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


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=64), nullable=False, unique=True)
    password = Column(String(length=64), nullable=False)
    is_active = Column(Boolean, default=True)
    profile_id = Column(ForeignKey("profile.id"), nullable=True)

    profile = relationship("Profile", back_populates="user", uselist=False)


class Profile(BaseModel):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=256), nullable=True)

    user = relationship("User", back_populates="profile")
