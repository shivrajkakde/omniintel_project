from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pickle
import numpy as np

app = FastAPI(
    title="OmniIntel Enterprise API",
    description="Backend engine connecting FastAPI, Scikit-Learn, and Streamlit.",
    version="2.0"
)

# Load the trained machine learning model safely on startup
MODEL_PATH = "delay_model.pkl"
ml_model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)
    print("SUCCESS: Trained ML model loaded successfully.")
else:
    print("WARNING: delay_model.pkl not found! Please run trainedmodel.py first.")

# Define input schema matching your database features
class ShipmentInput(BaseModel):
    shipping_cost: float
    delivery_time_days: int

@app.get("/")
def home():
    return {"message": "Welcome to OmniIntel Enterprise API. Backend is running successfully!"}

@app.post("/predict")
def predict_delay(data: ShipmentInput):
    if ml_model is None:
        raise HTTPException(status_code=500, detail="ML model is not loaded. Run trainedmodel.py first.")
    
    # Prepare input array for the model
    features = np.array([[data.shipping_cost, data.delivery_time_days]])
    
    # Make prediction
    prediction = int(ml_model.predict(features)[0])
    probability = float(ml_model.predict_proba(features)[0][1]) if hasattr(ml_model, "predict_proba") else 0.0
    
    status = "Delayed / High Risk" if prediction == 1 else "On-Time / Low Risk"
    
    return {
        "prediction": prediction,
        "status": status,
        "delay_probability": round(probability * 100, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)