from typing import Callable, Type, TypeVar

from fastapi import Depends

from api.dependencies.database import get_repository
from services.base import BaseService
from db.repositories.base import BaseRepository



def get_service(*, Service_type: Type[BaseService], Repo_type: Type[BaseRepository]) -> Callable:
    def _get_service(repo: BaseRepository = Depends(get_repository(Repo_type))) -> Type[BaseService]:
        return Service_type(repo)
    
    return _get_service