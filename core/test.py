import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict():
    data = {
        "concavity_mean": 0.3001,
        "concave_points_mean": 0.1471,
        "perimeter_se": 8.589,
        "area_se": 153.4,
        "texture_worst": 17.33,
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_get_result():
    # Assuming you have a way to get a valid task_id for testing
    task_id = "some_valid_task_id"
    response = client.get(f"/result/{task_id}")
    assert response.status_code == 200
    assert "status" in response.json()