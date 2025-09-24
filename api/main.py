from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import pickle
import logging
from typing import List

# ------------------------------
# Load the trained model
# ------------------------------
try:
    model = pickle.load(open("model/car_price_predictor_model.pkl", 'rb'))
except FileNotFoundError:
    raise FileNotFoundError("Model file not found! Please check the path.")

# ------------------------------
# Configure logging
# ------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ------------------------------
# Initialize FastAPI app
# ------------------------------
app = FastAPI(
    title="🚗 Car Price Predictor API",
    description="Predict car prices based on year, kilometers driven, fuel type, transmission, and ownership.",
    version="1.0"
)

# Allow all origins (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Pydantic model for input
# ------------------------------
class CarInput(BaseModel):
    Year: int = Field(..., ge=1990, le=2030, description="Year of manufacture")
    Kms_Driven: int = Field(..., ge=0, description="Kilometers driven")
    Present_Price: float = Field(..., ge=0, description="Current price in lacs")
    Fuel_Type: int = Field(..., ge=0, le=2, description="0=CNG, 1=Diesel, 2=Petrol")
    Transmission: int = Field(..., ge=0, le=1, description="0=Automatic, 1=Manual")
    Owner: int = Field(..., ge=0, le=3, description="0=First, 1=Second, 2=Third, 3=Fourth")

# ------------------------------
# Root endpoint
# ------------------------------
@app.get("/", tags=["Home"])
def read_root():
    """
    Root endpoint to check if API is running
    """
    return {"message": "🚗 Car Price Predictor API is running!"}

# ------------------------------
# Prediction endpoint
# ------------------------------
@app.post("/predict", tags=["Prediction"])
def predict_price(input_data: CarInput):
    """
    Predict the price of a car based on input parameters.
    """
    try:
        data = [[
            input_data.Year,
            input_data.Kms_Driven,
            input_data.Present_Price,
            input_data.Fuel_Type,
            input_data.Transmission,
            input_data.Owner
        ]]
        prediction = model.predict(data)
        logging.info(f"Prediction requested: {input_data.dict()} -> {prediction[0]}")
        return {"prediction_lakhs": round(float(prediction[0]), 2), "status": "success"}
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed. Check input data or model.")

# ------------------------------
# Run the API
# ------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
