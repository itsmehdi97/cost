import asyncio

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer

import aio_pika

from database import Session
import schemas
import jwt_utils
import consumer


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
        'prop.*',
        consumer.on_prop_msg,
        queue='props_changes'))


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
