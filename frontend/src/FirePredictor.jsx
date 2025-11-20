import React, { useEffect, useState } from "react";
import axios from "axios";

export default function PredictionTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/get-predicted-data")
      .then((res) => setData(res.data))
      .catch((err) => console.error("Lỗi khi lấy dữ liệu dự đoán:", err));
  }, []);

  return (
    <div>
      <h2>Kết quả dự đoán từ file CSV</h2>
      <table>
        <thead>
          <tr>
            <th>STT</th>
            <th>Nhiệt độ</th>
            <th>Độ ẩm</th>
            <th>TVOC</th>
            <th>eCO2</th>
            <th>Dự đoán</th>
            <th>Xác suất cháy (%)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td>{i + 1}</td>
              <td>{row["Temperature [C]"]}</td>
              <td>{row["Humidity [%]"]}</td>
              <td>{row["TVOC [ppb]"]}</td>
              <td>{row["eCO2 [ppm]"]}</td>
              <td>{row.prediction === 1 ? "🔥 Nguy cơ" : "✅ An toàn"}</td>
              <td>{row["prob_fire_true_%"]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
