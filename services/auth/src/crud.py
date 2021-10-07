from sqlalchemy.orm import session
import models
import schemas
import utils
from database import Session


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # TODO: Hash password
    user.password = utils.hash_password(user.password)
    db_user = models.User(**user.dict(), profile_id=None)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user