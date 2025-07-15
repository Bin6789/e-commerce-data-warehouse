from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import csv
import os

def load_csv_to_postgres():
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        dbname="dbname",  # Chú ý đúng với docker-compose
        user="user",
        password="password"
    )
    cur = conn.cursor()

    with open('/opt/airflow/datasets/marketing_campaign.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # bỏ dòng tiêu đề
        for row in reader:
            # ép dữ liệu về đúng kiểu, nếu cần
            row[0] = int(row[0])           # campaign_id
            row[5] = float(row[5])         # budget
            cur.execute(
                """
                INSERT INTO dim_campaign (
                    campaign_id, campaign_name, channel, start_date, end_date, budget
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                tuple(row)
            )

    conn.commit()
    cur.close()
    conn.close()

default_args = {
    'start_date': datetime(2025, 1, 1),
}

with DAG('load_marketing_campaign_csv',
         schedule_interval=None,
         catchup=False,
         default_args=default_args,
         tags=['csv', 'batch'],
         description='Load marketing_campaign.csv to DWH'
         ) as dag:

    load_task = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres
    )
