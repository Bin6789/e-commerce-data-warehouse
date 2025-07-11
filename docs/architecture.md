# Documentation
## 1. Thành phần chính của kiến trúc
### Data Sources (Nguồn dữ liệu):
- MySQL (Orders DB): Cơ sở dữ liệu quan hệ chứa thông tin về đơn hàng.
- API (FakeStore API): Giao diện API cung cấp dữ liệu giả lập (mock data).
- CSV (Marketing Data): Tệp CSV chứa dữ liệu marketing.
- Web Logs (Clickstream): Nhật ký truy cập web ghi lại hành vi người dùng (clickstream data).
=> Đây là điểm khởi đầu, nơi dữ liệu thô được thu thập từ các hệ thống hoặc nguồn bên ngoài.
### Kafka Streaming (Events, Logs):
- Hệ thống streaming dựa trên Apache Kafka, xử lý dữ liệu thời gian thực như sự kiện (events) và log.
- Vai trò là nguồn dữ liệu bổ sung, cung cấp luồng dữ liệu liên tục từ các sự kiện hoặc nhật ký hệ thống.
### Data Ingestion Pipelines (Pipeline thu thập dữ liệu):
- Quá trình thu thập và truyền dữ liệu từ các nguồn (Data Sources và Kafka Streaming) vào hệ thống.
- Sử dụng các pipeline để đảm bảo dữ liệu được tích hợp và chuyển tiếp hiệu quả.
### Data Lake (S3 / HDFS, Parquet):
- Kho lưu trữ dữ liệu thô hoặc bán cấu trúc, sử dụng: S3: Dịch vụ lưu trữ đám mây của AWS/HDFS: Hệ thống tệp phân tán của Hadoop/Parquet: Định dạng tệp tối ưu hóa cho lưu trữ cột (columnar storage).
- Lưu trữ dữ liệu trước khi xử lý thêm.
### Spark (Batch/Streaming) Data Processing & ETL:
- Công cụ Apache Spark xử lý dữ liệu theo lô (batch) hoặc thời gian thực (streaming).
- Thực hiện ETL (Extract, Transform, Load), bao gồm:
- Trích xuất dữ liệu từ Data Lake.
- Chuyển đổi (transformation) như làm sạch, tích hợp, và chuẩn hóa.
- Nạp (load) dữ liệu vào kho dữ liệu.
### Data Warehouse (Postgres/ Snowflake) (Star Schema):
- Kho dữ liệu (Data Warehouse) sử dụng: Postgres: Cơ sở dữ liệu quan hệ mở rộng/Snowflake: Nền tảng kho dữ liệu đám mây.
- Sử dụng mô hình Star Schema (sơ đồ sao) để tối ưu hóa truy vấn và phân tích.
### BI Tools (Superset, PowerBI):
- Công cụ Business Intelligence để trực quan hóa và phân tích dữ liệu: Superset: Nền tảng BI mã nguồn mở/PowerBI: Công cụ BI của Microsoft.
- Cung cấp báo cáo, dashboard và phân tích cho người dùng.
## 2. Cách thức hoạt động của từng thành phần
- Data Sources: Dữ liệu từ MySQL, API, CSV, và Web Logs được trích xuất theo định kỳ hoặc theo thời gian thực thông qua các kết nối API hoặc công cụ ETL.
- Kafka Streaming: Thu thập dữ liệu thời gian thực (events, logs) và truyền trực tiếp vào pipeline thu thập dữ liệu.
- Data Ingestion Pipelines: Sử dụng các công cụ như Apache NiFi hoặc Kafka Connect để thu thập dữ liệu từ các nguồn và Kafka, đảm bảo dữ liệu được truyền vào Data Lake một cách ổn định.
- Data Lake: Lưu trữ dữ liệu thô dưới dạng Parquet trên S3 hoặc HDFS, cho phép truy cập linh hoạt và xử lý phân tán.
- Spark: Xử lý dữ liệu theo lô (batch processing) hoặc thời gian thực (streaming processing) bằng các công cụ như Spark SQL hoặc Spark Streaming.Thực hiện các tác vụ ETL, bao gồm làm sạch dữ liệu, tích hợp từ nhiều nguồn, và chuẩn hóa định dạng.
- Data Warehouse: Lưu trữ dữ liệu đã xử lý dưới dạng Star Schema, tối ưu hóa cho các truy vấn phức tạp từ BI Tools. Postgres và Snowflake cung cấp khả năng mở rộng và hiệu suất cao.
- BI Tools: Truy vấn dữ liệu từ Data Warehouse để tạo báo cáo, biểu đồ, và dashboard. Superset và PowerBI hỗ trợ trực quan hóa dữ liệu cho người dùng cuối.
## 3. Quy trình hoạt động (Luồng dữ liệu)
### Thu thập dữ liệu (Extract):
- Dữ liệu từ Data Sources (MySQL, API, CSV, Web Logs) và Kafka Streaming (Events, Logs) được trích xuất.
- Luồng dữ liệu bắt đầu từ hai nguồn này, di chuyển qua Data Ingestion Pipelines.
- Lưu trữ thô (Initial Storage):
- Dữ liệu từ pipeline được truyền vào Data Lake (S3 / HDFS, Parquet), nơi nó được lưu trữ dưới dạng thô hoặc bán cấu trúc.
- Xử lý dữ liệu (Transform):
### Spark xử lý dữ liệu từ Data Lake, thực hiện các tác vụ ETL:
- Làm sạch dữ liệu (xóa giá trị null, sửa lỗi).
- Tích hợp dữ liệu từ các nguồn khác nhau.
- Chuyển đổi dữ liệu thành định dạng phù hợp với Star Schema.
### Lưu trữ và phân tích (Load & Analyze):
- Dữ liệu đã xử lý được nạp vào Data Warehouse (Postgres/Snowflake) với cấu trúc Star Schema.
- BI Tools (Superset, PowerBI) truy vấn dữ liệu từ Data Warehouse để tạo báo cáo và phân tích cho người dùng.