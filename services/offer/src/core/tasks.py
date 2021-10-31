
from typing import Callable
from fastapi import FastAPI

from db.tasks import connect_to_db, close_db_connection
from broker.tasks import connect_to_broker, close_broker_connection



def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)
        await connect_to_broker(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_broker_connection(app)
        await close_db_connection(app)

    return stop_app