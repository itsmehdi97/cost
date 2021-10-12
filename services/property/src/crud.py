import models
import schemas
from database import Session


def create_property(db: Session, property: schemas.PropertyCreate):
    db_prop = models.Property(**property.dict())
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop


def get_property(db: Session, user_id: int, title: str):
    return db.query(models.Property).filter(
        models.Property.user_id == user_id,
        models.Property.title == title
    ).first()
