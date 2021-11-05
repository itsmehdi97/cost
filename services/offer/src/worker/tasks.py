from datetime import datetime
from asgiref.sync import async_to_sync

from worker.celery import app
import schemas
from db.repositories.offers import OfferRepository



@app.task
def accept_offer(offer_id: int):
    repo = OfferRepository(accept_offer.db)
    
    offer = async_to_sync(repo.get_by_id)(id=offer_id)
    
    new_offer = schemas.Offer.parse_obj(offer.__dict__)
    new_offer.accepted = True
    new_offer.accept_date = datetime.now()

    async_to_sync(repo.update)(offer=new_offer)
    print('### accepted', new_offer)
    return new_offer.json()