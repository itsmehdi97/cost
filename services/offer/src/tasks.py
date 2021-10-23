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
        exchange='offers'
    ):
    exc = await channel.get_exchange(exchange)
    msg = aio_pika.Message(
        body if isinstance(body, bytes) else bytes(body, encoding='utf-8'),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )
    print('# publishing msg', routing_key, body)
    await exc.publish(msg, routing_key=routing_key) 


async def offer_placed(conn: aio_pika.Connection, offer: schemas.Offer):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            offer.json(),
            'offer.place')


async def offer_updated(conn: aio_pika.Connection, offer: schemas.Offer):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            offer.json(),
            'offer.update')


async def offer_canceled(conn: aio_pika.Connection, offer: schemas.Offer):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            offer.json(),
            'offer.cancel')


async def offer_accepted(conn: aio_pika.Connection, offer: schemas.Offer):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            offer.json(),
            'offer.accept')
