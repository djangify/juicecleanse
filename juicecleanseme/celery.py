import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juicecleanseme.settings')

# instantiate Celery
app = Celery('juicecleanseme')

# load settings from Django settings, using CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks from installed apps
app.autodiscover_tasks()