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

## 📅 Ngày: 2025-07-18
### ✅ Task Completed:
- Sửa lại cấu trúc thư mục dự án và cấu trúc etl.
- Tạo DAG 'generate_test_data.py' để sinh dữ liệu test và lưu dữ liệu vào datasets.
- Sử dụng Faker để tạo dữ liệu ngẫu nhiên cho các bảng.
- Cập nhật Dockerfile để cài đặt Faker.
- Tạo DAG load dữ liệu vào raw dim tables
- Chạy DAG thành công, dữ liệu đã được nạp vào các bảng trong PostgreSQL
- Kiểm tra dữ liệu trong PostgreSQL để xác nhận.
- Commit code và push lên GitHub với tag `v1.0-day5`

### 🚩 Issues/Blockers:
- Chú ý việc load dữ liệu vào các bảng raw dim tables, cần đảm bảo không trùng lặp dữ liệu.
- Cần kiểm tra kỹ các trường dữ liệu để tránh lỗi khi sinh dữ liệu.
- Chưa load được clickstream data và campaign data, vào fact_clickstream và fact_campaign_result.
### 🔥 Next Plan:
- Cập nhật các DAG để xử lý dữ liệu clickstream và campaign.
- Xử lý dữ liệu được ingest từ API và Database MySQL.

### 💡 Notes/Learning
- Học được cách sử dụng Faker để sinh dữ liệu ngẫu nhiên cho các bảng trong PostgreSQL.
- Biết cách cập nhật Dockerfile để cài đặt các thư viện Python cần thiết.
- Hiểu rõ hơn về cách tổ chức cấu trúc thư mục trong dự án ETL.
- Cách sử dụng DAG trong Airflow để tự động hóa quá trình nạp dữ liệu
- Cách sử dụng PostgresHook để kết nối và thao tác với PostgreSQL trong Airflow.
- Cách sử dụng BashOperator để chạy các lệnh hệ thống trong Airflow.
- Cách sử dụng PythonOperator để chạy các hàm Python trong Airflow.
