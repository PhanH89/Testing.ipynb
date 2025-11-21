import React, { useState } from "react";
import axios from "axios";
import "./FirePredictor.css";
export default function PredictionForm() {
  const [formData, setFormData] = useState({
    Temperature_C: "",
    Humidity_percent: "",
    TVOC_ppb: "",
    eCO2_ppm: "",
    Raw_H2: "",
    Raw_Ethanol: "",
    Pressure_hPa: "",
    PM1_0: "",
    PM2_5: "",
    NC0_5: "",
    NC1_0: "",
    NC2_5: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // gửi dữ liệu JSON sang backend
      const res = await axios.post("http://localhost:8000/predict", formData);
      setResult(res.data);
    } catch (error) {
      console.error("Lỗi gửi dữ liệu:", error);
      alert("Không thể gửi dữ liệu đến server.");
    }
  };

  return (
    <div className="page">
      <div className="card">
        <div>
          <h2>Nhập dữ liệu cảm biến</h2>
          <form onSubmit={handleSubmit}>
            {Object.keys(formData).map((key) => (
              <div key={key} style={{ marginBottom: "8px" }}>
                <label>{key}: </label>
                <input
                  type="number"
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  placeholder="Nhập số"
                  required
                />
              </div>
            ))}
            <button type="submit">Dự đoán</button>
          </form>

          {result && (
            <div style={{ marginTop: "20px" }}>
              <h3>Kết quả dự đoán:</h3>
              <p>
                Dự đoán:{" "}
                {result.prediction === 1 ? "🔥 Nguy cơ cháy" : "✅ An toàn"}
              </p>
              <p>Xác suất cháy: {result["probability_fire_%"]}%</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
