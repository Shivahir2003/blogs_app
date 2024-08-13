import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')

app = Celery('blogsite')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-mail-every-day-for-blogs' : {
        'task': 'blogapp.tasks.send_mail_for_new_blogs',
        'schedule' : crontab(hour='*/24')
    },
    'delete_completed_tasks' : {
        'task': 'blogapp.tasks.clear_task_result',
        'schedule' : crontab(minute=0, hour=0),
    }
}
