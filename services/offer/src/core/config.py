from typing import Optional
from functools import lru_cache

from databases import DatabaseURL
from pydantic import BaseSettings



class Settings(BaseSettings):
    WORKER_THREADS: int
    SECRET_KEY: str
    DB_USER: str
    DB_PASSWORD: str
    DB_SERVER: str
    DB_PORT: str
    DATABASE: str

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DATABASE}"


    class Config:
        env_file = ".env"



@lru_cache
def get_settings():
    return Settings()