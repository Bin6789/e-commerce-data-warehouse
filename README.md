# E-Commerce Data Warehouse Project

## Mục tiêu
Xây dựng hệ thống Data Warehouse cho e-commerce, hỗ trợ ingest, ETL, phân tích dữ liệu, và trực quan hóa với Metabase.

## Thành phần chính
- **Postgres**: Lưu trữ data warehouse (dwh) và metadata cho Metabase.
- **MySQL**: Lưu trữ dữ liệu nguồn.
- **Airflow**: Orchestrate các pipeline ETL.
- **Spark**: Xử lý dữ liệu lớn.
- **Kafka**: Streaming data.
- **FastAPI**: API phục vụ sinh dữ liệu test và ingest.
- **Metabase**: Trực quan hóa dữ liệu.

## Cấu trúc thư mục
- `airflow_dags/`: DAGs cho Airflow (ingest, ETL, load fact...)
- `connectors/`: Connector cho Kafka Connect.
- `datasets/`: Dữ liệu mẫu (CSV, static...)
- `docker_env/`: Docker Compose, Dockerfile, scripts khởi tạo DB.
- `docs/`: Tài liệu kiến trúc, hướng dẫn.
- `fastapi_server/`: Source code FastAPI.
- `processing/`: Scripts xử lý dữ liệu.
- `warehouse/schema/`: Schema SQL cho data warehouse.

## Khởi động hệ thống
1. **Cấu hình RAM/CPU cho Docker Desktop** (khuyến nghị >= 4GB RAM).
2. **Chạy lệnh:**
   ```sh
   docker compose down -v
   docker compose up -d
   ```
3. Truy cập các service:
   - Metabase: http://localhost:3000
   - FastAPI: http://localhost:8000
   - Airflow: http://localhost:8080
   - Spark UI: http://localhost:8081

## Lưu ý
- **Metabase** sử dụng database riêng (`metabase_db`), không mount schema SQL vào DB này.
- **Các file SQL schema** chỉ mount vào DB `dwh`.
- **Script tạo nhiều DB**: `docker_env/init/create_metabase_db.sh`.
- **Cấu hình RAM/CPU** cho từng service trong `docker-compose.yml` bằng `mem_limit` và `cpus`.

## Đóng góp
- Fork repo, tạo branch mới, PR về main.
- Đọc thêm trong `docs/`.

## Liên hệ
- Chủ project: Bin6789
- Email: [your-email@example.com]