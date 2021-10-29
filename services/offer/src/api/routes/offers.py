from fastapi import APIRouter, Depends

from schemas.offer import Offer
from api.dependencies.database import get_repository
from db.repositories.offers import OfferRepository



router = APIRouter()


        
@router.get("/{offer_id}", response_model=Offer)
async def get_offer(
        offer_id: int,
        offers_repo: OfferRepository = Depends(get_repository(OfferRepository))
    ):
    return await offers_repo.get_offer_by_id(id=offer_id)


# @router.post("/place-offer")
# async def create_offer(
#         offer: schemas.OfferCreate,
#         bg_tasks: BackgroundTasks,
#         db: Session = Depends(get_db),
#         user: schemas.User = Depends(current_user)
#     ):
#     if not user.id == offer.user_id:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid user_id",
#         )

#     if crud.get_offer(db, prop_id=offer.prop_id, user_id=offer.user_id):
#         raise HTTPException(
#             status_code=400,
#             detail="Offer already exists",
#         )       


#     db_offer = crud.create_offer(db, offer)

#     bg_tasks.add_task(
#         tasks.offer_placed, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

#     return db_offer


# @router.put("/update-offer/{offer_id}")
# async def update_offer(
#         offer_id: int,
#         bg_tasks: BackgroundTasks,
#         offer: schemas.OfferUpdate,
#         db: Session = Depends(get_db),
#         user: schemas.User = Depends(current_user)
#     ):
#     if not offer_id == offer.id:
#         raise HTTPException(
#             status_code=400,
#             detail="invalid offer_id",
#         )

#     db_offer = crud.get_offer_by_id(db, offer_id)
#     if not db_offer:
#         raise HTTPException(
#             status_code=404,
#             detail="offer not found",
#         )

#     if not user.id == db_offer.user_id:
#         raise HTTPException(
#             status_code=403,
#             detail="not allowed to update this offer",
#         )
    

#     if not offer.prop_id == db_offer.prop_id:
#         raise HTTPException(
#             status_code=400,
#             detail="only price is updatable",
#         ) 

#     crud.update_offer(db, offer)
#     db.refresh(db_offer)

#     bg_tasks.add_task(
#         tasks.offer_updated, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

#     return db_offer


# @router.delete("/cancel-offer/{offer_id}")
# async def update_offer(
#         offer_id: int,
#         bg_tasks: BackgroundTasks,
#         db: Session = Depends(get_db),
#         user: schemas.User = Depends(current_user)
#     ):

#     db_offer = crud.get_offer_by_id(db, offer_id)
#     if not db_offer:
#         raise HTTPException(
#             status_code=404,
#             detail="offer not found",
#         )

#     if not user.id == db_offer.user_id:
#         raise HTTPException(
#             status_code=403,
#             detail="not allowed to cancel this offer",
#         )
    
#     if not db_offer.canceled:
#         offer = schemas.OfferUpdate.parse_obj(db_offer.__dict__)
#         offer.canceled = True

#         crud.update_offer(db, offer)
#         db.refresh(db_offer)

#         bg_tasks.add_task(
#             tasks.offer_canceled, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

#     return db_offer