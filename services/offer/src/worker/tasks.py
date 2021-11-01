from celery import Celery

from core.config import get_settings



settings = get_settings()

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery.task
def add(x: int, y: int) -> int:
    return x + y