from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2

def load_csv_to_postgres():
    df = pd.read_csv('/opt/airflow/datasets/marketing_campaign.csv')
    conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO dim_campaign (campaign_id, campaign_name, channel, start_date, end_date, budget)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (campaign_id) DO NOTHING
            """,
            tuple(row)
        )
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id='load_marketing_campaign_csv',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["csv", "campaign"]
) as dag:
    load_task = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres
    )
