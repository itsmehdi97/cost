from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.database import get_repository
from api.dependencies.services import get_service
from services.offer import OfferService 
from api.dependencies.auth import current_user
from db.repositories.offers import OfferRepository
import schemas



router = APIRouter()

        
@router.get("/{offer_id}", response_model=schemas.Offer)
async def get_offer(
        offer_id: int,
        offers_repo: OfferRepository = Depends(get_repository(OfferRepository))
    ):
    return await offers_repo.get_by_id(id=offer_id)


@router.post("/place", response_model=schemas.Offer)
async def place_offer(
        offer: schemas.OfferCreate,
        # bg_tasks: BackgroundTasks,
        offers_svc: OfferService = Depends(get_service(Service_type=OfferService, Repo_type=OfferRepository)),
        user: schemas.User = Depends(current_user)
    ):
    db_offer = await offers_svc.place(offer=offer, requesting_user=user)

    # bg_tasks.add_task(
    #     tasks.offer_placed, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

    return db_offer


@router.put("/update/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        # bg_tasks: BackgroundTasks,
        offer: schemas.OfferUpdate,
        offers_svc: OfferService = Depends(get_service(Service_type=OfferService, Repo_type=OfferRepository)),
        user: schemas.User = Depends(current_user)
    ):
    db_offer = await offers_svc.update(id=offer_id, offer=offer, requesting_user=user)

    # bg_tasks.add_task(
    #     tasks.offer_updated, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

    return db_offer


@router.put("/cancel/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        # bg_tasks: BackgroundTasks,
        offers_svc: OfferService = Depends(get_service(Service_type=OfferService, Repo_type=OfferRepository)),
        user: schemas.User = Depends(current_user)
    ):
    db_offer = await offers_svc.cancel(id=offer_id, requesting_user=user)

    # bg_tasks.add_task(
    #     tasks.offer_canceled, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

    return db_offer