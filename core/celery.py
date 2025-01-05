from celery import Celery

# Create a Celery instance
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()