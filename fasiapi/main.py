from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model và scaler
model = joblib.load("model/model.joblib")
scaler = joblib.load("model/scaler.joblib")

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "predicted_results.csv")

class SmokeData(BaseModel):
    Temperature_C: float
    Humidity_percent: float
    TVOC_ppb: float
    eCO2_ppm: float
    Raw_H2: float
    Raw_Ethanol: float | None = 0
    Pressure_hPa: float
    PM1_0: float
    PM2_5: float
    NC0_5: float | None = 0
    NC1_0: float
    NC2_5: float

@app.post("/predict")
def predict(data: SmokeData):
    input_data = [
        data.Temperature_C,
        data.Humidity_percent,
        data.TVOC_ppb,
        data.eCO2_ppm,
        data.Raw_H2,
        data.Raw_Ethanol or 0,
        data.Pressure_hPa,
        data.PM1_0,
        data.PM2_5,
        data.NC0_5 or 0,
        data.NC1_0,
        data.NC2_5
    ]

    X = np.array([input_data])
    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1] * 100

    # Lưu kết quả vào output/predicted_results.csv
    df_result = pd.DataFrame([input_data], columns=[
        "Temperature_C", "Humidity_percent", "TVOC_ppb", "eCO2_ppm",
        "Raw_H2", "Raw_Ethanol", "Pressure_hPa",
        "PM1_0", "PM2_5","NC0_5", "NC1_0", "NC2_5"
    ])
    df_result["prediction"] = prediction
    df_result["probability_fire_%"] = round(probability, 2)
    df_result.to_csv(OUTPUT_FILE, index=False)

    return {
        "prediction": int(prediction),
        "probability_fire_%": round(probability, 2)
    }