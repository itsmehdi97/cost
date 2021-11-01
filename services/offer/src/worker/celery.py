from celery import Celery

from core.config import get_settings



settings = get_settings()

app = Celery(__name__)
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.autodiscover_tasks(packages=['worker'], related_name='tasks')