from functools import lru_cache

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
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DATABASE}?min_size={2}&max_size={int(self.WORKER_THREADS)*2}"

    class Config:
        env_file = ".env"



@lru_cache
def get_settings():
    return Settings()