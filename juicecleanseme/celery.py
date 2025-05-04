import os
from celery import Celery

# This must match your Django project directory name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juicecleanseme.settings')

# The Celery app name should also use 'juicecleanseme'
app = Celery('juicecleanseme')

# Load any custom configuration from settings
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()