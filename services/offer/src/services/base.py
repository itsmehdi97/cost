from fastapi import BackgroundTasks

from db.repositories.base import BaseRepository
from broker.publishers import Publisher



class BaseService:
    def __init__(self, *, repo: BaseRepository, publisher: Publisher, bg_tasks: BackgroundTasks):
        self.repo = repo
        self.publisher = publisher
        self.bg_tasks = bg_tasks