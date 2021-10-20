import aio_pika

from typing import Union

import schemas



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


async def property_added(conn: aio_pika.Connection, prop: schemas.PropertyUpdate):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            prop.json(),
            'prop.add')


async def property_updated(conn: aio_pika.Connection, prop: schemas.Property):
    async with conn.channel() as ch:
        await _publish_msg(
            ch,
            prop.json(),
            'prop.updated')
