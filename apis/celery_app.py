from celery import Celery
import time

celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery_app.task
def create_task():
    time.sleep(10)  # Simulação de uma tarefa demorada
    return "Task completed!"
