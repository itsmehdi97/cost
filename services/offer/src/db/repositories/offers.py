from sqlalchemy import select

from db.repositories.base import BaseRepository
from models.offers import Offer




class OfferRepository(BaseRepository):
    async def get_offer_by_id(self, *, id: int):
        query = select(Offer).where(Offer.id == id)
        db_offer = await self.db.fetch_one(query=str(query), values={'id_1': id})

        return Offer(**db_offer) if db_offer else None
