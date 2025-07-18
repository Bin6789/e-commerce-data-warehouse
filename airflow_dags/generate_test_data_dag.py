from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
import random
from faker import Faker

fake = Faker()
DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datasets'))

def generate_csv_files(**kwargs):
    os.makedirs(DATASET_DIR, exist_ok=True)

    # Lấy số lượng dòng từ biến môi trường hoặc mặc định
    row_count = kwargs.get('dag_run').conf.get('row_count', 10000) if kwargs.get('dag_run') else 10000

    # Danh sách để tránh trùng lặp
    used_ids = set()

    # 1. Users
    users = []
    for i in range(1, row_count + 1):
        users.append({
            "user_id": i,
            "name": fake.name(),
            "email": fake.email(),
            "created_at": fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S'),
        })
        used_ids.add(i)
    pd.DataFrame(users).to_csv(f"{DATASET_DIR}/customer.csv", index=False)

    # 2. Products
    products = []
    for i in range(row_count + 1, row_count * 2 + 1):  # Dùng phạm vi khác để tránh trùng
        products.append({
            "product_id": i,
            "product_name": fake.word().capitalize(),
            "category": random.choice(["electronics", "clothing", "home", "toys"]),
            "price": round(random.uniform(5, 500), 2),
        })
        used_ids.add(i)
    pd.DataFrame(products).to_csv(f"{DATASET_DIR}/product.csv", index=False)

    # 3. Campaigns
    campaigns = []
    for i in range(row_count * 2 + 1, row_count * 3 + 1):
        campaigns.append({
            "campaign_id": i,
            "campaign_name": fake.catch_phrase(),
            "channel": random.choice(["Email", "Social Media", "Google Ads"]),
            "start_date": fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
            "end_date": fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            "budget": random.randint(1000, 20000),
        })
        used_ids.add(i)
    pd.DataFrame(campaigns).to_csv(f"{DATASET_DIR}/marketing_campaign.csv", index=False)

    # 4. Orders
    orders = []
    for i in range(row_count * 3 + 1, row_count * 4 + 1):
        user_id = random.choice(list(used_ids.intersection(range(1, row_count * 4 + 1))))
        product_id = random.choice(list(used_ids.intersection(range(row_count + 1, row_count * 2 + 1))))
        orders.append({
            "order_id": i,
            "user_id": user_id,
            "product_id": product_id,
            "order_date": fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            "quantity": random.randint(1, 5),
            "total_amount": round(random.uniform(20, 1000), 2),
        })
        used_ids.add(i)
    pd.DataFrame(orders).to_csv(f"{DATASET_DIR}/order.csv", index=False)

    # 5. Clickstream
    clickstream = []
    for _ in range(row_count):
        user_id = random.choice(list(used_ids.intersection(range(1, row_count + 1))))
        clickstream.append({
            "event_time": fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S'),
            "user_id": user_id,
            "session_id": fake.uuid4(),
            "page_url": fake.uri_path(),
            "device_type": random.choice(["mobile", "desktop", "tablet"]),
        })
    pd.DataFrame(clickstream).to_csv(f"{DATASET_DIR}/clickstream_logs.csv", index=False)

    print(f"✅ Generated all CSV files with {row_count} rows into {DATASET_DIR}")

default_args = {
    'start_date': datetime(2025, 1, 1),
}

with DAG('generate_test_data_dag',
         default_args=default_args,
         schedule_interval=None,
         catchup=False,
         tags=['dev', 'test', 'csv'],
         description='Generate synthetic e-commerce CSV test data') as dag:

    generate_data = PythonOperator(
        task_id='generate_csv_data',
        python_callable=generate_csv_files,
        provide_context=True  # Cho phép truyền tham số từ UI
    )