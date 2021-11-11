from datetime import datetime

from models.offers import Offer
from db.repositories.base import BaseRepository
import schemas



class OfferRepository(BaseRepository):
    async def get_by_id(self, *, id: int) -> Offer:
        return self.db.query(Offer) \
            .filter(Offer.id == id) \
            .first()

    async def get(self, *, prop_id: int, user_id: int) -> Offer:
        return self.db.query(Offer) \
            .filter(
                Offer.prop_id == prop_id,
                Offer.user_id == user_id) \
            .first()

    async def create(self, *,offer: schemas.OfferCreate):
        db_offer = Offer(**offer.dict())
        self.db.add(db_offer)
        self.db.commit()
        self.db.refresh(db_offer)
        return db_offer

    async def update(self, *, offer: schemas.OfferUpdate):
        values = offer.dict()
        values['updated_at'] = datetime.now()

        self.db.query(Offer) \
            .filter(Offer.id == offer.id) \
            .update(values, synchronize_session=False)
        self.db.commit()

        return await self.get_by_id(id=offer.id)

    async def get_max_offered_price(self, *, prop_id: int):
        offer = self.db.query(Offer) \
            .filter(Offer.prop_id == prop_id) \
            .order_by(Offer.price.desc()) \
            .first()
        
        return offer.price if offer else None