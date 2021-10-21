from typing import Callable, Any, Optional

from aio_pika import Connection, IncomingMessage

import tasks
import schemas
from database import Session



async def start_consuming(
        conn: Connection,
        exchange: str,
        binding_key: str,
        cb: Callable[[IncomingMessage], Any],
        queue: str = None
    ):
    async with conn.channel() as channel:
        await channel.set_qos(prefetch_count=1)
        exc = await channel.get_exchange(exchange, ensure=True)
        q = await channel.declare_queue(
            name=queue,
            durable=False,
            exclusive=False,
            passive=False,
            auto_delete=False)

        print(f'# queue {queue} is bound to exchange {exchange} with {binding_key} key.')
        await q.bind(exc, routing_key=binding_key)
        print(f'# consuming from {queue}...')
        while True:
            await q.consume(cb)


async def on_prop_msg(msg: IncomingMessage):
    msg_type = msg.routing_key.split('.')[1]

    db = Session()
    try:
        if msg_type == 'transfer':
            await tasks.property_transferred(
                db, schemas.PropertyTransfer.parse_raw(msg.body))
            msg.ack()

        else:
            print('# Unknown prop message type: %r' % msg_type)
        
    finally:
        db.close()
