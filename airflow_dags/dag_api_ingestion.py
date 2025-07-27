# airflow_dags/dag_api_ingestion.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from raw_ingestion.api.load_user_api import load_users_from_api
from raw_ingestion.api.load_product_api import load_products_from_api
from raw_ingestion.api.load_order_api import load_orders_from_api
from raw_ingestion.api.load_clickstream_api import load_clickstream_from_api

default_args = {
    'start_date': datetime(2025, 1, 1)
}

with DAG('dag_api_ingestion',
         schedule_interval=None,
         catchup=False,
         default_args=default_args,
         tags=['api', 'raw', 'ingestion'],
         description='Ingest user/product/order/clickstream from API into raw_* tables'
         ) as dag:

    task_users = PythonOperator(
        task_id='ingest_users_from_api',
        python_callable=load_users_from_api
    )

    task_products = PythonOperator(
        task_id='ingest_products_from_api',
        python_callable=load_products_from_api
    )

    task_orders = PythonOperator(
        task_id='ingest_orders_from_api',
        python_callable=load_orders_from_api
    )

    task_clickstream = PythonOperator(
        task_id='ingest_clickstream_from_api',
        python_callable=load_clickstream_from_api
    )

    [task_users, task_products, task_orders] >> task_clickstream
