from typing import Callable, Any
import functools
import asyncio
import logging

from aio_pika import IncomingMessage, Connection

from db.repositories.base import BaseRepository



logger = logging.getLogger(__name__)


class BaseConsumer:
    def __init__(self, broker_conn: Connection):
        self.broker_conn = broker_conn

    async def start_consuming(self, repo: BaseRepository, *,
        exchange: str,
        binding_key: str,
        cb: Callable[[BaseRepository, IncomingMessage], Any],
        queue: str = None
    ):
        async def _start_consuming():
            async with self.broker_conn.channel() as channel:
                await channel.set_qos(prefetch_count=1)
                exc = await channel.get_exchange(exchange, ensure=True)
                q = await channel.declare_queue(
                    name=queue,
                    durable=False,
                    exclusive=False,
                    passive=False,
                    auto_delete=False)

                logger.info(f'# queue {queue} is bound to exchange {exchange} with {binding_key} key.')
                await q.bind(exc, routing_key=binding_key)
                logger.info(f'# consuming from {queue}...')
                
                while True:
                    await q.consume(
                        functools.partial(cb, repo))

        asyncio.create_task(_start_consuming())