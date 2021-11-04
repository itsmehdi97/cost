from fastapi import HTTPException

from services.base import BaseService
import schemas
import models
from worker import tasks



class OfferService(BaseService):
    async def place(self, *, offer: schemas.Offer, requesting_user: schemas.User) -> models.Offer:
        if not requesting_user.id == offer.user_id:
            raise HTTPException(
                status_code=400,
                detail="Invalid user_id",
            )
        
        if await self.repo.get(prop_id=offer.prop_id, user_id=offer.user_id):
            raise HTTPException(
                status_code=400,
                detail="Offer already exists",
            )

        db_offer = await self.repo.create(offer=offer)
        self.bg_tasks.add_task(
            self.publisher.publish,
            body=schemas.Offer.parse_obj(db_offer.__dict__).json(),
            routing_key='offer.place',
            exchange='offers')

        self.bg_tasks.add_task(
            tasks.accept_offer.delay,
            db_offer.id)

        return db_offer

    async def update(self, *, id: int, offer: schemas.Offer, requesting_user: schemas.User) -> models.Offer:
        if not id == offer.id:
            raise HTTPException(
                status_code=400,
                detail="invalid offer_id",
            )

        db_offer = await self.repo.get_by_id(id=id)
        if not db_offer:
            raise HTTPException(
                status_code=404,
                detail="offer not found",
            )

        if not requesting_user.id == db_offer.user_id:
            raise HTTPException(
                status_code=403,
                detail="not allowed to update this offer",
            )

        if not offer.prop_id == db_offer.prop_id:
            raise HTTPException(
                status_code=400,
                detail="only price is updatable",
            )
        
        db_offer = await self.repo.update(offer=offer)
        if db_offer:
            self.bg_tasks.add_task(
                self.publisher.publish,
                body=schemas.Offer.parse_obj(db_offer.__dict__).json(),
                routing_key='offer.update',
                exchange='offers')

        return db_offer

    async def cancel(self, *, id: int, requesting_user: schemas.User):
        db_offer = await self.repo.get_by_id(id=id)
        if not db_offer:
            raise HTTPException(
                status_code=404,
                detail="offer not found",
            )

        if not requesting_user.id == db_offer.user_id:
            raise HTTPException(
                status_code=403,
                detail="not allowed to cancel this offer",
            )
        
        if not db_offer.canceled:
            offer = schemas.OfferUpdate.parse_obj(db_offer.__dict__)
            offer.canceled = True

            db_offer = await self.repo.update(offer=offer)

            self.bg_tasks.add_task(
                self.publisher.publish,
                body=schemas.Offer.parse_obj(db_offer.__dict__).json(),
                routing_key='offer.cancel',
                exchange='offers')

        return db_offer
        