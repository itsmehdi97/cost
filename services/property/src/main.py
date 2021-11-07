import json
import logging
import asyncio

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

import crud
import schemas
from database import Session
import jwt_utils
import tasks
import consumer

import aio_pika


app = FastAPI()


rabbit_conn = None

@app.on_event("startup")
async def startup_event():
    global rabbit_conn
    
    print('# Connecting to rabbitmq broker')

    rabbit_conn = await aio_pika.connect_robust(host='queue') 
    async with rabbit_conn.channel() as ch:
        await ch.declare_exchange('props', type='topic', durable=True)

    #TODO: number of consumers bound to gunicorn worker threads.
    asyncio.create_task(
        consumer.start_consuming(
            rabbit_conn,
            'props',
            'prop.transfer',
            consumer.on_prop_msg,
            queue='props_ownership_trans'))


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
    return Response(status_code=204)



@app.post("/properties/", response_model=schemas.Property)
async def create_property(
        property: schemas.PropertyCreate,
        bg_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(current_user)
    ):
    db_prop = crud.get_property(db, user.id, property.title)
    if db_prop:
        raise HTTPException(
            status_code=400,
            detail="property already exists",
        )

    property.user_id = user.id
    new_prop = crud.create_property(db, property)

    bg_tasks.add_task(
        tasks.property_added, rabbit_conn, schemas.Property(**new_prop.__dict__))

    return new_prop


@app.put("/properties/{prop_id}", response_model=schemas.Property)
async def update_property(
        prop_id: int,
        bg_tasks: BackgroundTasks,
        prop: schemas.PropertyUpdate,
        user: schemas.User = Depends(current_user),
        db: Session = Depends(get_db)
    ):
        if crud.get_property(db, user.id, prop.title):
            raise HTTPException(
                status_code=400,
                detail="property already exists",
            )

        db_prop = crud.get_property_by_id(db, prop_id)
        if not db_prop:
            raise HTTPException(
                status_code=404,
                detail="Property not found"
            )
        
        if not db_prop.user_id == user.id:
            raise HTTPException(
                status_code=403,
                detail="Not allowed to update this property"
            )
        
        crud.update_property(db, prop)
        print(db_prop)
        db.refresh(db_prop)

        bg_tasks.add_task(
            tasks.property_updated, rabbit_conn, schemas.Property(**db_prop.__dict__))

        return db_prop
