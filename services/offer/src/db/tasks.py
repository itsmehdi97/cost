from fastapi import FastAPI
from databases import Database

from core.config import get_settings

import logging



logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    config = get_settings()
    database = Database(
        config.DATABASE_URL, min_size=2, max_size=int(config.WORKER_THREADS)*2)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
