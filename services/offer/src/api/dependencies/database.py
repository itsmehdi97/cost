from typing import Callable, Type

from db import Session
from starlette.requests import Request
from fastapi import Depends

from db.repositories.base import BaseRepository




def get_db(request: Request):
    db = request.app.state._db()
    try:
        yield db
    finally:
        db.close()


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Session = Depends(get_db)) -> Type[BaseRepository]:
        return Repo_type(db)

    return get_repo