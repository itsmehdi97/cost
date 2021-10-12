import os
from typing import Optional

from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import JWTError, jwt

import crud
import schemas
import config



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY = os.environ.get("SECRET", "Super Secret")
# ALGORITHM = "HS256"


def get_user(db, username):
    u = crud.get_user_by_username(db, username)
    return schemas.UserInDb(**u.__dict__) if u else None


def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    settings = config.get_settings()

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
