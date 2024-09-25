from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from apis.celery_app import create_task  # Certifique-se de usar o caminho correto

app = FastAPI()

# Rota para iniciar o processamento
@app.post("/start-task/")
async def start_task(background_tasks: BackgroundTasks):
    task = create_task.delay()
    return {"task_id": task.id, "status": "Processing started"}

# Rota para verificar o status da tarefa
@app.get("/task-status/{task_id}")
async def task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {"task_id": task_id, "status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"task_id": task_id, "status": "Failed"}
    else:
        return {"task_id": task_id, "status": task_result.state}
