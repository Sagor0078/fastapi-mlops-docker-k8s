from celery import Celery
from utils.functions import get_model_response

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task(name="tasks.get_model_response_task")
def get_model_response_task(data):
    return get_model_response(data)