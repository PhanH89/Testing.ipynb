from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/get-predicted-data")
def get_predicted_data():
    try:
        df = pd.read_csv("output/predicted_results.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
@app.get("/predict-all-csv")
def predict_all_csv():
    # Load dữ liệu
    df = pd.read_csv("data/smoke_dataset.csv")

    # Load scaler và model
    scaler = joblib.load("model/scaler.joblib")
    model = joblib.load("model/model.joblib")

    # Chọn cột đầu vào
    features = [
        "Temperature [C]", "Humidity [%]", "TVOC [ppb]", "eCO2 [ppm]",
        "Raw H2", "Raw Ethanol", "Pressure [hPa]",
        "PM1.0", "PM2.5", "NC0.5", "NC1.0", "NC2.5"
    ]
    X = df[features]

    # Chuẩn hóa dữ liệu
    X_scaled = scaler.transform(X)

    # Dự đoán
    preds = model.predict(X_scaled)
    probs = model.predict_proba(X_scaled)[:, 1] * 100

    # Gộp kết quả
    df["prediction"] = preds
    df["prob_fire_true_%"] = probs.round(2)

    # Tạo thư mục output nếu chưa có
    os.makedirs("output", exist_ok=True)

    # Lưu ra file CSV
    output_path = "output/predicted_results.csv"
    df.to_csv(output_path, index=False)

    # Trả về file CSV
    return FileResponse(output_path, media_type="text/csv", filename="predicted_results.csv")