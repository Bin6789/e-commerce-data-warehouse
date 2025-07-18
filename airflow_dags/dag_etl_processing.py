from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from transform.generate_dim_date import generate_dim_date
from transform.raw_to_dim_user import transform_users
from transform.raw_to_dim_product import transform_products
from transform.raw_to_dim_campaign import transform_campaigns
from transform.raw_to_dim_clickstream import transform_clickstream

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
}

with DAG(
    dag_id='dag_etl_processing',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['etl', 'dim'],
    description='ETL từ raw -> dim (users, products, campaigns, clickstream, dim_date)',
) as dag:

    task_generate_dim_date = PythonOperator(
        task_id='generate_dim_date',
        python_callable=generate_dim_date,
    )

    task_transform_users = PythonOperator(
        task_id='transform_users',
        python_callable=transform_users,
    )

    task_transform_products = PythonOperator(
        task_id='transform_products',
        python_callable=transform_products,
    )

    task_transform_campaigns = PythonOperator(
        task_id='transform_campaigns',
        python_callable=transform_campaigns,
    )

    task_transform_clickstream = PythonOperator(
        task_id='transform_clickstream',
        python_callable=transform_clickstream,
    )

    # Thiết lập thứ tự phụ thuộc giữa các task
    task_generate_dim_date >> [
        task_transform_users,
        task_transform_products,
        task_transform_campaigns,
        task_transform_clickstream
    ]
