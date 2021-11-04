import weakref
from asgiref.sync import async_to_sync

from celery import Celery

import schemas
from db.repositories.offers import OfferRepository
import models
from core.config import get_settings
from db.tasks import connect_to_db
from db import Session


class CustomCeleryApp(Celery):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = connect_to_db()
        #TODO: close db connection
        
settings = get_settings()

app = CustomCeleryApp(__name__)
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.autodiscover_tasks(packages=['worker'], related_name='tasks')