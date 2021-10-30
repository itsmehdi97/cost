from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

import aio_pika

from database import Session
import jwt_utils
import schemas
import crud
import tasks



app = FastAPI()


rabbit_conn = None

@app.on_event("startup")
async def startup_event():
    global rabbit_conn
    
    print('# Connecting to rabbitmq broker')

    rabbit_conn = await aio_pika.connect_robust(host='queue') 
    async with rabbit_conn.channel() as ch:
        await ch.declare_exchange('offers', type='topic', durable=True)


@app.on_event("shutdown")
async def shutdown_event():
    print('# Closing rabbitmq connection')
    await rabbit_conn.close()


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
        bg_tasks: BackgroundTasks,
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

    bg_tasks.add_task(
        tasks.offer_placed, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

    return db_offer


@app.put("/update-offer/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        bg_tasks: BackgroundTasks,
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

    bg_tasks.add_task(
        tasks.offer_updated, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

    return db_offer


@app.delete("/cancel-offer/{offer_id}", response_model=schemas.Offer)
async def update_offer(
        offer_id: int,
        bg_tasks: BackgroundTasks,
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

        bg_tasks.add_task(
            tasks.offer_canceled, rabbit_conn, schemas.Offer.parse_obj(db_offer.__dict__))

    return db_offer
