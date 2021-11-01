from typing import Union
import logging

import aio_pika



logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, channel: aio_pika.Channel):
        self.channel = channel

    async def publish(self, *, body: Union[str, bytes], routing_key: str, exchange: str) -> None:
        try:
            exc = await self.channel.get_exchange(exchange)
            msg = aio_pika.Message(
                body if isinstance(body, bytes) else bytes(body, encoding='utf-8'),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )

            logger.debug('### publishing msg ###')
            logger.debug('body: ', body)
            logger.debug('routing key: ', routing_key)
            logger.debug('exchange: ', exchange)
            logger.debug('### publishing msg ###')

            await exc.publish(msg, routing_key=routing_key)
        finally:
            await self.channel.close()