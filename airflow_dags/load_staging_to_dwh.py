from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
from pathlib import Path

sys.path.append('/opt/airflow/ingestion/db_extractor')
from staging_to_dwh import extract_and_load

default_args = {
    'start_date': datetime(2025, 1, 1)
}

with DAG('load_staging_to_dwh',
         schedule_interval=None,
         catchup=False,
         default_args=default_args,
         tags=['db_ingest', 'staging'],
         description='Load data from staging-db to DWH'
         ) as dag:

    extract_task = PythonOperator(
        task_id='transfer_data_from_staging',
        python_callable=extract_and_load
    )
