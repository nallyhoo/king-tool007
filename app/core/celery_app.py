from celery import Celery
from kombu import Queue

REDIS_URL = "redis://localhost:6379/0"

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.video_tasks"], 
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_queues = (
        Queue('high_priority', routing_key='high_priority'),
        Queue('normal_priority', routing_key='normal_priority'),
        Queue('low_priority', routing_key='low_priority'),
    ),
    task_default_queue = 'normal_priority',
)
