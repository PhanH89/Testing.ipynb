🚀 Giới thiệu Back-end (Fasiapi)
Backend được xây dựng bằng FastAPI. Nhiệm vụ chính:
• 	Đọc dữ liệu từ file 'smoke_dataset.csv'
• 	Chuẩn hóa dữ liệu bằng 'scaler.joblib'
• 	Dự đoán nguy cơ cháy bằng mô hình 'model.joblib'
• 	Xuất kết quả ra file 'predicted_results.csv' và cung cấp API để frontend hiển thị
⚙️ Cài đặt
1. **Tạo môi trường ảo**
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
2. **Cài đặt dependencies**
pip install -r requirements.txt
3. **requirements.txt (thư viện python)**
- fastapi
- uvicorn
- pandas
- numpy
- joblib
- scikit-learn
4. **Chạy server**
uvicorn main:app --reload
Api docs: http://localhost:8000/docs 
Route chính:
• 	/predict-all-csv → Xuất file CSV kết quả dự đoán
• 	/get-predicted-data → Trả về dữ liệu CSV dưới dạng JSON để frontend render
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🚀 Giới thiệu FrontEnd (frontend)
Frontend được xây dựng bằng ReactJS. Nhiệm vụ chính:
• 	Gọi API từ backend
• 	Hiển thị dữ liệu dự đoán
⚙️ Cài đặt
1. 	**Cài đặt dependencies**
npm install
2. 	**Chạy ứng dụng**
npm start

