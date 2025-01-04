from pydantic import BaseModel, Field
from typing_extensions import Literal
from fastapi import FastAPI, BackgroundTasks

from celery.result import AsyncResult

model_name = "Breast Cancer Wisconsin (Diagnostic)"
version = "v1.0.0"

app = FastAPI()

class BreastData(BaseModel):
    concavity_mean: float = Field(..., gt=0)
    concave_points_mean: float = Field(..., gt=0)
    perimeter_se: float = Field(..., gt=0)
    area_se: float = Field(..., gt=0)
    texture_worst: float = Field(..., gt=0)
    area_worst: float = Field(..., gt=0)

    class Config:
        schema_extra = {
            "concavity_mean": 0.3001,
            "concave_points_mean": 0.1471,
            "perimeter_se": 8.589,
            "area_se": 153.4,
            "texture_worst": 17.33,
            "area_worst": 2019.0,
        }

class BreastPrediction(BaseModel):
    label: Literal["M", "B"]

from celery_app import celery_app

@app.post("/predict")
async def predict(data: BreastData, background_tasks: BackgroundTasks):
    task = celery_app.send_task("tasks.get_model_response_task", args=[data.dict()])
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "Pending"}
    elif task_result.state != 'FAILURE':
        return {"status": task_result.state, "result": task_result.result}
    else:
        return {"status": "Failure", "result": str(task_result.info)}