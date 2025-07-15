# Project Diary

Project logs go here.

## 📅 Ngày: 2025-07-11
### ✅ Task Completed:
- Tạo repo dự án.
- Hiểu sơ về kiến trúc tổng thể dự án Data Warehouse.
- Viết file 'docs/architecture.md' mô tả kiến trúc dự án.
- Vẽ sơ đồ kiến trúc dự án bằng draw.io.
- Tạo repo GitHub, clone repo về máy.
- Copy toàn bộ dự án & datasets vào repo.
- Thiết lập `.gitignore` chuẩn cho dự án.
- Tạo branch `feature/initial-setup` để commit project structure.
- Commit code & push lên GitHub.
- Mở Pull Request, merge về branch `develop`.

### 🚩 Issues/Blockers:
- None

### 🔥 Next Plan:
- Setup Docker Compose, chạy thử môi trường Data Platform.

### 💡 Notes/Learning:
- Học được cách tổng quan một hệ thống Data Platform.
- Biết rằng mỗi phần có vai trò riêng, phải kết nối nhịp nhàng.
- Biết cách quản lý GitHub repo theo chuẩn team Data Engineering.
- Học được cách dùng branch, commit, pull request chuyên nghiệp.

## 📅 Ngày: 2025-07-13
### ✅ Task Completed:
- Cài Docker Compose (nếu cần).
- Khởi chạy các container: Kafka, Postgres, Airflow, Spark.
- Truy cập Airflow Web UI thành công.

### 🚩 Issues/Blockers:
- None

### 🔥 Next Plan:
- Kiểm tra kết nối Kafka → Airflow (sẽ thực hiện ở Ngày 3).

### 💡 Notes/Learning:
- Biết cách dùng Docker để mô phỏng một hệ thống Big Data hoàn chỉnh.
- Airflow Web UI rất trực quan để quản lý DAG.

## 📅 Ngày: 2025-07-15
### ✅ Task Completed:
- Cập nhật Docker Compose file với các phiên bản mới nhất của Airflow và Postgres
- Chạy lại các container với cấu hình mới.
- Tạo các bảng Star Schema trong PostgreSQL
- Viết DAG `load_csv_to_postgres.py` dùng BashOperator và lệnh COPY
- Nạp dữ liệu từ thư mục `airflow_dags/data/`
- DAG đã chạy thành công trong Airflow UI
- Đã commit & push với tag `v1.0-day3`
### 🚩 Issues/Blockers:
- Không có vấn đề lớn, chỉ cần chú ý đến phiên bản Docker images.
### 🔥 Next Plan:
- Real-time Streaming bằng Kafka & Spark
### 💡 Notes/Learning
- Học được cách sử dụng BashOperator trong Airflow để chạy lệnh hệ thống.
- Biết cách nạp dữ liệu từ file CSV vào PostgreSQL bằng lệnh COPY.