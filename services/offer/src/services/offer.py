from datetime import datetime, timedelta

from fastapi import HTTPException

from services.base import BaseService
import schemas
import models
from worker import tasks
from core.config import get_settings



settings = get_settings()


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
            self._schedule_accept_task,
            offer=db_offer,
            eta=db_offer.created_at + timedelta(minutes=settings.OFFER_ACCEPT_DELAY),
            requesting_user=requesting_user)

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
        
        if not db_offer.status == models.OfferStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail=f"offer cannot ne updated at this state ({db_offer.status})",
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
            offer.status = models.OfferStatus.CANCELED

            db_offer = await self.repo.update(offer=offer)

            self.bg_tasks.add_task(
                self.publisher.publish,
                body=schemas.Offer.parse_obj(db_offer.__dict__).json(),
                routing_key='offer.cancel',
                exchange='offers')

        return db_offer


    async def _schedule_accept_task(self, *, offer: models.Offer, eta: datetime, requesting_user: schemas.User):
            res = tasks.accept_offer.apply_async((offer.id,), eta=eta)
            accepting_offer = schemas.Offer.parse_obj(offer.__dict__)
            accepting_offer.task_id = res.task_id

            await self.repo.update(offer=accepting_offer)