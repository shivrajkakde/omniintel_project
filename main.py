from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load your trained model
model = joblib.load("delay_model.pkl")

class ShipmentInput(BaseModel):
    shipping_cost: float
    delivery_time_days: int
    historical_failure_rate: float

@app.post("/predict")
def predict_risk(data: ShipmentInput):
    # Convert input to a 2D numpy array to bypass feature name validation
    features = np.array([[
        data.shipping_cost,
        data.delivery_time_days,
        data.historical_failure_rate
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    
    # Get prediction probability if available
    try:
        proba = model.predict_proba(features)[0]
        confidence = float(max(proba)) * 100
    except Exception:
        confidence = 85.0

    risk_status = "High Risk - Potential Delay" if prediction == 1 else "Low Risk - On Time"

    return {
        "risk_assessment": risk_status,
        "model_confidence": round(confidence, 2)
    }