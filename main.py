from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load your trained model
model = joblib.load("delay_model.pkl")

class ShipmentInput(BaseModel):
    shipping_cost: float
    delivery_time_days: int
    historical_failure_rate: float

@app.post("/predict")
def predict_risk(data: ShipmentInput):
    # Prepare input dataframe for the model
    input_df = pd.DataFrame([{
        "shipping_cost": data.shipping_cost,
        "delivery_time_days": data.delivery_time_days,
        "historical_failure_rate": data.historical_failure_rate
    }])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    
    # Get prediction probability if available
    try:
        proba = model.predict_proba(input_df)[0]
        confidence = float(max(proba)) * 100
    except Exception:
        confidence = 85.0

    risk_status = "High Risk - Potential Delay" if prediction == 1 else "Low Risk - On Time"

    return {
        "risk_assessment": risk_status,
        "model_confidence": round(confidence, 2)
    }