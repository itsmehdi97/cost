from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

from database import Session
import jwt_utils
import schemas
import crud



app = FastAPI()



@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# TODO:
SECRET = "SECRET_KEY"


async def current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt_utils.verify_token(token, SECRET)
    if payload:
        return schemas.User(id=payload.get('uid'), username=payload.get('sub'))
    raise HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/ping")
async def ping():
    return Response(status_code=200)


@app.post("/place-offer", response_model=schemas.Offer)
async def create_offer(
        offer: schemas.OfferCreate,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(current_user)
    ):
    if not user.id == offer.user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id",
        )

    if crud.get_offer(db, prop_id=offer.prop_id, user_id=offer.user_id):
        raise HTTPException(
            status_code=400,
            detail="Offer already exists",
        )       


    db_offer = crud.create_offer(db, offer)
    return db_offer


@app.put("/update-offer/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        offer: schemas.OfferUpdate,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(current_user)
    ):
    if not offer_id == offer.id:
        raise HTTPException(
            status_code=400,
            detail="invalid offer_id",
        )

    db_offer = crud.get_offer_by_id(db, offer_id)
    if not db_offer:
        raise HTTPException(
            status_code=404,
            detail="offer not found",
        )

    if not user.id == db_offer.user_id:
        raise HTTPException(
            status_code=403,
            detail="not allowed to update this offer",
        )
    

    if not offer.prop_id == db_offer.prop_id:
        raise HTTPException(
            status_code=400,
            detail="only price is updatable",
        ) 

    crud.update_offer(db, offer)
    db.refresh(db_offer)

    return db_offer


@app.delete("/cancel-offer/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(current_user)
    ):

    db_offer = crud.get_offer_by_id(db, offer_id)
    if not db_offer:
        raise HTTPException(
            status_code=404,
            detail="offer not found",
        )

    if not user.id == db_offer.user_id:
        raise HTTPException(
            status_code=403,
            detail="not allowed to cancel this offer",
        )
    
    if not db_offer.canceled:
        offer = schemas.OfferUpdate.parse_obj(db_offer.__dict__)
        offer.canceled = True

        crud.update_offer(db, offer)
        db.refresh(db_offer)

    return db_offer
