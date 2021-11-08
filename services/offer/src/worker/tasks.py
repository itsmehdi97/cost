from datetime import datetime, timedelta
from asgiref.sync import async_to_sync

import schemas
import models
from worker.celery import app
from db.repositories.offers import OfferRepository
from core.config import get_settings


settings = get_settings()


@app.task(ignore_result=True)
def accept_offer(offer_id: int):
    repo = OfferRepository(accept_offer.db)
    
    offer = async_to_sync(repo.get_by_id)(id=offer_id)
    
    new_offer = schemas.Offer.parse_obj(offer.__dict__)
    new_offer.accept_date = datetime.now()
    new_offer.status = models.OfferStatus.ACCEPTED

    res = transfer_offer.apply_async((offer_id,), eta=new_offer.accept_date + timedelta(minutes=settings.OFFER_TRANSFER_DELAY))
    new_offer.task_id = res.task_id

    async_to_sync(repo.update)(offer=new_offer)
    accept_offer.publisher.publish_sync(
        body=new_offer.json(),
        routing_key='offer.accept',
        exchange='offers')

    return new_offer.json()


@app.task(ignore_result=True)
def transfer_offer(offer_id: int):
    repo = OfferRepository(transfer_offer.db)

    offer = async_to_sync(repo.get_by_id)(id=offer_id)
    new_offer = schemas.Offer.parse_obj(offer.__dict__)
    new_offer.transfer_date = datetime.now()
    new_offer.status = models.OfferStatus.TRANSFERRED

    async_to_sync(repo.update)(offer=new_offer)
    accept_offer.publisher.publish_sync(
        body=new_offer.json(),
        routing_key='offer.transfer',
        exchange='offers')

    return new_offer.json()