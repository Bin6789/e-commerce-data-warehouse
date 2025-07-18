from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from load_fact.load_fact_order import load_fact_orders
from load_fact.load_fact_campaign_result import load_fact_campaign_result
from load_fact.load_fact_clickstream import load_fact_clickstream

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
}

with DAG(
    dag_id='dag_load_fact',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['master', 'fact'],
    description='Load dữ liệu vào các bảng fact từ raw và dim',
) as dag:

    task_load_fact_orders = PythonOperator(
        task_id='load_fact_orders',
        python_callable=load_fact_orders,
    )

    task_load_fact_campaign = PythonOperator(
        task_id='load_fact_campaign_result',
        python_callable=load_fact_campaign_result,
    )

    task_load_fact_clickstream = PythonOperator(
        task_id='load_clickstream_fact',
        python_callable=load_fact_clickstream,
    )

    task_load_fact_orders >> [task_load_fact_campaign, task_load_fact_clickstream]
