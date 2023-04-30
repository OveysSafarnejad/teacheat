import os
import time

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teacheat.settings')

celery = Celery(__name__)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
celery.autodiscover_tasks()


@celery.task
def hello_celery_task(with_timeout: int) -> dict:
    time.sleep(with_timeout)
    return {"param_name": "with_timeout", "param_value": with_timeout}
