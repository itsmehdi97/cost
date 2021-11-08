import weakref
from asgiref.sync import async_to_sync

from celery import Celery
from celery import Task

import schemas
from db.repositories.offers import OfferRepository
import models
from core.config import get_settings
from db.tasks import connect_to_db
from broker.tasks import connect_to_broker_sync
from broker.publishers import Publisher
from db import Session



settings = get_settings()


class CustomTask(Task):
    _db = None
    _broker_conn = None

    @property
    def db(self):
        if self._db is None:
            self._db = connect_to_db()
        return self._db


    def get_publisher(self):
        if self._broker_conn is None:

            self._broker_conn = connect_to_broker_sync()
        
        print('sync', self._broker_conn)

        ch = self._broker_conn.channel()
        return Publisher(ch)
        
        

app = Celery(__name__, task_cls="worker.celery.CustomTask")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.autodiscover_tasks(packages=['worker'], related_name='tasks')