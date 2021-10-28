from functools import lru_cache

from pydantic import BaseSettings



class Settings(BaseSettings):
    OFFER_ACCEPT_DELAY=2
    

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()