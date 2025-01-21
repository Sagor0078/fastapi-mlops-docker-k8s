from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing_extensions import Literal
from core.utils import get_model_response

model_name = "Breast Cancer Wisconsin (Diagnostic)"
version = "v1.0.0"

app = FastAPI()

# Input for data validation
class BreastData(BaseModel):
    concavity_mean: float = Field(..., gt=0)
    concave_points_mean: float = Field(..., gt=0)
    perimeter_se: float = Field(..., gt=0)
    area_se: float = Field(..., gt=0)
    texture_worst: float = Field(..., gt=0)
    area_worst: float = Field(..., gt=0)

    class Config:
        # example data
        json_schema_extra = {
            "example": {
                "concavity_mean": 0.3001,
                "concave_points_mean": 0.1471,
                "perimeter_se": 8.589,
                "area_se": 153.4,
                "texture_worst": 17.33,
                "area_worst": 17.33,
            }
        }

# Output model
class BreastPrediction(BaseModel):
    prediction: Literal["benign", "malignant"]
    probability: float

@app.get("/info")
async def model_info():
    """Return model information, version, how to call"""
    return {"name": model_name, "version": version}

@app.get("/health")
async def service_health():
    """Return service health"""
    return {"ok"}

@app.post("/predict", response_model=BreastPrediction)
async def model_predict(sample: BreastData):
    """Predict with input"""
    response = get_model_response(sample)
    return response