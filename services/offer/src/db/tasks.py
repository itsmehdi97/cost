from fastapi import FastAPI

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from core.config import get_settings
from db import Session

import logging



logger = logging.getLogger(__name__)



def connect_to_db(app: FastAPI = None) -> Session:
    settings = get_settings()


    try:
        logger.info("making db engine...")
        engine = create_engine(settings.DATABASE_URL)

        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        
        if app:
            app.state._db_engine = engine
            app.state._db = Session

        return Session

    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")
    



def close_db_connection(app: FastAPI) -> None:
    try:
        app.state._db_engine.dispose()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
