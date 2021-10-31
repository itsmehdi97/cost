from db.repositories.base import BaseRepository


class BaseService:
    def __init__(self, repo: BaseRepository):
        self.repo = repo