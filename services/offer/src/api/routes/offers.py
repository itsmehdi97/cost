from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from services.offer import OfferService 
from broker.publishers import Publisher
from db.repositories.offers import OfferRepository
import schemas
from api.dependencies import ( 
    get_repository,
    get_service,
    current_user,
    get_publisher
)


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
        offers_svc: OfferService = Depends(get_service(Service_type=OfferService, Repo_type=OfferRepository)),
        user: schemas.User = Depends(current_user),
    ):
    return await offers_svc.place(offer=offer, requesting_user=user)


@router.put("/update/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        offer: schemas.OfferUpdate,
        offers_svc: OfferService = Depends(get_service(Service_type=OfferService, Repo_type=OfferRepository)),
        user: schemas.User = Depends(current_user),
    ):
    return await offers_svc.update(id=offer_id, offer=offer, requesting_user=user)


@router.put("/cancel/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        offers_svc: OfferService = Depends(get_service(Service_type=OfferService, Repo_type=OfferRepository)),
        user: schemas.User = Depends(current_user),
    ):
    return await offers_svc.cancel(id=offer_id, requesting_user=user)