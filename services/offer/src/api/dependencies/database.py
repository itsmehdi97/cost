from typing import Callable, Type

from databases import Database
from starlette.requests import Request
from fastapi import Depends

from db.repositories.base import BaseRepository



def get_database(request: Request):
    return request.app.state._db


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)

    return get_repo