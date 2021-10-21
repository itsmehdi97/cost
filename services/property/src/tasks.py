from typing import Union
from datetime import datetime

import aio_pika

import schemas
import models
from database import Session



async def _publish_msg(
        channel: aio_pika.Channel,
        body: Union[str, bytes],
        routing_key: str,
        exchange='props'
    ):
    exc = await channel.get_exchange(exchange)
    msg = aio_pika.Message(
        body if isinstance(body, bytes) else bytes(body, encoding='utf-8'),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )
    print('# publishing msg', routing_key, body)
    await exc.publish(msg, routing_key=routing_key) 


async def property_added(conn: aio_pika.Connection, prop: schemas.Property):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            prop.json(),
            'prop.add')


async def property_updated(conn: aio_pika.Connection, prop: schemas.Property):
    print('publishing', prop)
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            prop.json(),
            'prop.update')


async def property_transferred(db: Session, prop: schemas.PropertyTransfer):
    print('## Applying Transfer ---> ', prop)

    values = {
        'user_id': prop.user_id,
        'price': prop.price,
        'transfer_date': datetime.now()
    }    
    
    db.query(models.Property) \
        .filter(models.Property.id == prop.id) \
        .update(values, synchronize_session=False)
    db.commit()
