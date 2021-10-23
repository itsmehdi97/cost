from datetime import datetime

import schemas
import models
from database import Session



def get_offer(db: Session, prop_id: int, user_id: int):
    return db.query(models.Offer) \
        .filter(
            models.Offer.prop_id == prop_id,
            models.Offer.user_id == user_id) \
        .first()


def get_offer_by_id(db: Session, offer_id: int):
    return db.query(models.Offer) \
        .filter(models.Offer.id == offer_id) \
        .first()


def create_offer(db: Session, offer: schemas.OfferCreate):
    db_offer = models.Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def update_offer(db: Session, offer: schemas.OfferUpdate):
    values = offer.dict()
    values['updated_at'] = datetime.now()

    update_count = db.query(models.Offer) \
        .filter(models.Offer.id == offer.id) \
        .update(values, synchronize_session=False)
    db.commit()

    return update_count