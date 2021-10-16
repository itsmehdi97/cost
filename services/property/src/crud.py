from datetime import datetime
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


def get_property_by_id(db: Session, prop_id: str):
    return db.query(models.Property).filter(models.Property.id == prop_id).first()


def update_property(db: Session, prop: schemas.PropertyUpdate):
    values = prop.dict()
    values['updated_at'] = datetime.now()
    update_count = db.query(models.Property) \
        .filter(models.Property.id == prop.id) \
        .update(values, synchronize_session=False)
    db.commit()
    return update_count