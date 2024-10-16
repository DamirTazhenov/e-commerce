import os
from celery import Celery
from kombu import Exchange, Queue



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('eccomerce')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('emails', Exchange('emails'), routing_key='emails'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'