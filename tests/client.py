import json

import requests

url = "http://0.0.0.0:8000/predict"
headers = {"Content-Type": "application/json"}
data = {
    "concavity_mean": 0.3001,
    "concave_points_mean": 0.1471,
    "perimeter_se": 8.589,
    "area_se": 153.4,
    "texture_worst": 17.33,
    "area_worst": 2019.0,
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.json())
