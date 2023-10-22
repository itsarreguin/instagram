import os

from django.conf import settings

from celery import Celery

from dotenv import load_dotenv; load_dotenv()


# Set the default Django settings module for the 'celery' program.
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ['PROJECT_SETTINGS'])


celery = Celery('instagram')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
celery.autodiscover_tasks()