from typing import Callable, Type, TypeVar

from starlette.requests import Request
from fastapi import Depends

from api.dependencies.database import get_repository
from services.base import BaseService
from db.repositories.base import BaseRepository
from broker.publishers import Publisher



def get_service(*, Service_type: Type[BaseService], Repo_type: Type[BaseRepository]) -> Callable:
    def _get_service(repo: BaseRepository = Depends(get_repository(Repo_type))) -> Type[BaseService]:
        return Service_type(repo)
    
    return _get_service


async def get_publisher(request: Request) -> Publisher:
    broker_conn = request.app.state._broker_conn
    return Publisher(
        await broker_conn.channel())