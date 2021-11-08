import aio_pika
from core.config import get_settings

import logging


logger = logging.getLogger(__name__)

async def connect_to_broker(app):
    settings = get_settings()
    try:
        connection = await aio_pika.connect_robust(host=settings.BROKER_HOST) 
        app.state._broker_conn = connection
        async with connection.channel() as ch:
            await ch.declare_exchange('offers', type='topic', durable=True)
            await ch.declare_exchange('props', type='topic', durable=True)
    except Exception as e:
        logger.warn('--- BROKER CONNECTION ERROR ---')
        logger.warn(e)
        logger.warn('--- BROKER CONNECTION ERROR ---')

        raise e


async def close_broker_connection(app):
    try:
        await app.state._broker_conn.close()
    except Exception as e:
        logger.warn('--- BROKER DISCONNECT ERROR ---')
        logger.warn(e)
        logger.warn('--- BROKER DISCONNECT ERROR ---')  