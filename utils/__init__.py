# Imports
import joblib
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Load model
model = joblib.load("model/model_binary.dat.gz")
