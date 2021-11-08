import aio_pika
import pika
from core.config import get_settings

import logging


logger = logging.getLogger(__name__)

async def connect_to_broker(app=None):
    settings = get_settings()
    try:
        connection = await aio_pika.connect_robust(host=settings.BROKER_HOST) 
        if app:
            app.state._broker_conn = connection
        async with connection.channel() as ch:
            await ch.declare_exchange('offers', type='topic', durable=True)
            await ch.declare_exchange('props', type='topic', durable=True)

        return connection
    except Exception as e:
        logger.warn('--- BROKER CONNECTION ERROR ---')
        logger.warn(e)
        logger.warn('--- BROKER CONNECTION ERROR ---')

        raise e

def connect_to_broker_sync():
    print('########### CONNECTING SYNC ##')
    settings = get_settings()
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.BROKER_HOST))
        ch = connection.channel()
        ch.exchange_declare(exchange='offers', exchange_type='topic', durable=True)
        ch.exchange_declare(exchange='props', exchange_type='topic', durable=True)
        print('########### CONNECTING SYNC ##', connection)

        return connection
    except Exception as e:
        logger.warn('--- BROKER CONNECTION ERROR ---')
        logger.warn(e)
        logger.warn('--- BROKER CONNECTION ERROR ---')


async def close_broker_connection(app):
    try:
        await app.state._broker_conn.close()
    except Exception as e:
        logger.warn('--- BROKER DISCONNECT ERROR ---')
        logger.warn(e)
        logger.warn('--- BROKER DISCONNECT ERROR ---')  