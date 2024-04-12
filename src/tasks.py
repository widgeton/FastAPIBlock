from celery import Celery
from celery.schedules import crontab
import redis as r

from config import settings
from main import CACHE_PREFIX

redis = r.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)

celery = Celery("tradings", broker=settings.REDIS_URL)

celery.conf.beat_schedule = {
    "run-every-day_in_14_11": {
        "task": "tasks.clean_cache",
        "schedule": crontab(hour='14', minute='11')
    }
}


@celery.task
def clean_cache():
    keys = redis.keys(f"{CACHE_PREFIX}*")
    if keys:
        redis.delete(*keys)
