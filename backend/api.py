from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model

app = FastAPI()

model = load_model("models/lstm_eta.h5")

class ETAPredictRequest(BaseModel):
    speed_sequence: list[float]

@app.get("/")
def root():
    return {"status": "Smart Bus API Running"}

@app.post("/predict_eta")
def predict_eta(request: ETAPredictRequest):
    seq = np.array(request.speed_sequence).reshape(1, 10, 1)
    eta = model.predict(seq)
    return {"predicted_eta_minutes": float(eta[0][0])}
