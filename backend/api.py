from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# ML Model Loading
MODEL_PATH = 'backend/eta_model.pkl'
LE_BUS_PATH = 'backend/le_bus.pkl'
LE_STOP_PATH = 'backend/le_stop.pkl'

model = None
le_bus = None
le_stop = None

def load_model():
    global model, le_bus, le_stop
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        le_bus = joblib.load(LE_BUS_PATH)
        le_stop = joblib.load(LE_STOP_PATH)
        print("ML Model Loaded.")
    else:
        print("Model not found. Predictions will fail.")

load_model()

class PredictionRequest(BaseModel):
    bus_id: str
    stop_name: str
    scheduled_time: str # HH:MM

@app.get("/")
def home():
    return {"status": "ML API Active"}

@app.post("/predict")
def predict_eta(req: PredictionRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Preprocess features
        bus_code = le_bus.transform([req.bus_id])[0]
        stop_code = le_stop.transform([req.stop_name])[0]
        
        # Parse time
        time_obj = datetime.strptime(req.scheduled_time, "%H:%M")
        hour = time_obj.hour
        minute = time_obj.minute
        
        # Predict Delay
        features = pd.DataFrame([[bus_code, stop_code, hour, minute]], 
                              columns=['Bus_ID_Code', 'Stop_Code', 'Hour', 'Minute'])
        
        predicted_delay = model.predict(features)[0]
        
        # Calculate Historical Rating (1-5 Stars) based on predicted delay
        # If predicted delay is low, rating is high.
        # This simulates "historical performance" since the model is trained on history.
        if predicted_delay <= 0: rating = 5.0
        elif predicted_delay <= 5: rating = 4.5
        elif predicted_delay <= 10: rating = 4.0
        elif predicted_delay <= 15: rating = 3.0
        elif predicted_delay <= 30: rating = 2.0
        else: rating = 1.0
        
        # Calculate Adjusted ETA (just returning delay for now to add to base time)
        return {
            "bus_id": req.bus_id,
            "predicted_delay_min": round(predicted_delay, 2),
            "status": "Late" if predicted_delay > 5 else "On Time",
            "rating": rating
        }
        
    except Exception as e:
        print(f"Prediction Error: {e}")
        # Fallback if unknown bus/stop
        return {"predicted_delay_min": 0, "status": "Unknown (Fallback)"}

# Keeping minimal route data for reference if needed
@app.get("/routes")
def get_routes():
    # Placeholder for static route data
    return {"message": "Use Node.js for live route data"}
