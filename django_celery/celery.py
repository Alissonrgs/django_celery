from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

app = Celery('django_celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

beat_exchange = Exchange('beat', type='direct')
default_exchange = Exchange('default', type='direct')
transient_exchange = Exchange('transient', delivery_mode=1)

app.conf.task_queues = [
    Queue(
        'beat',
        beat_exchange,
        routing_key='beat',
        queue_arguments={'x-max-priority': 10}
    ),
    Queue(
        'default',
        default_exchange,
        routing_key='deafult',
        queue_arguments={'x-max-priority': 10}
    ),
    Queue('transient', transient_exchange, routing_key='transient')
]
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
