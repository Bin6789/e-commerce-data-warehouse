from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowException
from datetime import datetime
import pandas as pd
import os
import logging
from sqlalchemy import create_engine
import time

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Định nghĩa đường dẫn dữ liệu
DATA_DIR = '/opt/airflow/datasets/static'
BASE_DIR = os.path.abspath(DATA_DIR)

# Cấu hình mặc định
default_args = {
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': 10,
    'on_failure_callback': lambda context: logger.error(f"Task failed: {context['task_instance'].task_id}")
}

# Hàm tải dữ liệu CSV vào PostgreSQL với to_sql
def load_csv_to_postgres(**kwargs):
    task_id = kwargs['task_id']
    table_name = kwargs['table_name']
    csv_file = kwargs['csv_file']
    columns = kwargs['columns']
    conn_id = kwargs.get('conn_id', 'postgres_dwh')
    refresh_data = kwargs.get('refresh_data', False)

    try:
        file_path = os.path.join(BASE_DIR, csv_file)
        if not os.path.exists(file_path):
            raise AirflowException(f"File not found: {file_path}")

        csv_row_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
        logger.info(f"Total rows in {csv_file}: {csv_row_count}")

        chunksize = 10000
        pg_hook = PostgresHook(postgres_conn_id=conn_id)
        engine = create_engine(pg_hook.get_uri())

        if refresh_data:
            pg_hook.run(f"TRUNCATE TABLE {table_name} CASCADE")
            logger.info(f"Refreshed data in {table_name}")

        if_exists = 'replace' if refresh_data else 'append'
        total_rows = 0

        max_retries = 3
        for attempt in range(max_retries):
            try:
                for chunk in pd.read_csv(file_path, usecols=columns, chunksize=chunksize):
                    if chunk.empty:
                        logger.warning(f"No data in chunk for {csv_file}")
                        continue

                    # Cast kiểu dữ liệu cho các cột có trong CSV
                    for col in columns:
                        if col in chunk.columns:
                            if col in ['price', 'budget', 'rating_rate', 'total_amount', 'quantity']:
                                chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
                            elif col in ['created_at', 'order_date', 'event_time']:
                                chunk[col] = pd.to_datetime(chunk[col], errors='coerce', format='%Y-%m-%d %H:%M:%S')
                            elif col in ['start_date', 'end_date']:
                                chunk[col] = pd.to_datetime(chunk[col], errors='coerce', format='%Y-%m-%d').dt.date

                    # Ánh xạ cột cho raw_products
                    if table_name == 'raw_products':
                        if 'product_name' in chunk.columns:
                            chunk = chunk.rename(columns={'product_name': 'title'})
                        # Không điền giá trị mặc định, để các cột khác tự động là NULL

                    if table_name in ['raw_orders', 'raw_clickstreams']:
                        if 'user_id' in columns:
                            valid_user_ids = pd.read_sql("SELECT user_id FROM raw_users", engine)['user_id'].tolist()
                            chunk = chunk[chunk['user_id'].isin(valid_user_ids)]
                            if chunk.empty:
                                logger.warning(f"No valid user_ids in chunk for {csv_file}")
                                continue
                        if 'product_id' in columns and table_name == 'raw_orders':
                            valid_product_ids = pd.read_sql("SELECT product_id FROM raw_products", engine)['product_id'].tolist()
                            chunk = chunk[chunk['product_id'].isin(valid_product_ids)]
                            if chunk.empty:
                                logger.warning(f"No valid product_ids in chunk for {csv_file}")
                                continue

                    # Chèn dữ liệu, các cột không có sẽ tự động là NULL
                    chunk.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi')
                    total_rows += len(chunk)
                    logger.info(f"Loaded {len(chunk)} rows into {table_name}")
                    if_exists = 'append'

                break
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {task_id}: {str(e)}")
                if attempt < max_retries - 1:
                    logger.warning(f"Retrying in 10s...")
                    time.sleep(10)
                else:
                    raise

        if total_rows != csv_row_count:
            logger.warning(f"Mismatch: Expected {csv_row_count} rows, loaded {total_rows} rows into {table_name}")

        logger.info(f"Successfully loaded {total_rows} rows into {table_name}")
    except Exception as e:
        logger.error(f"Error loading {csv_file} into {table_name}: {str(e)}")
        raise
    finally:
        if 'engine' in locals():
            engine.dispose()

# Định nghĩa DAG
with DAG('load_raw_csv',
         default_args=default_args,
         schedule_interval=None,
         catchup=False,
         tags=['ingestion', 'csv', 'test'],
         description='Load raw data from CSV into raw tables in DWH') as dag:

    tasks = {
        'load_raw_users': {
            'table_name': 'raw_users',
            'csv_file': 'customer.csv',
            'columns': ['user_id', 'name', 'email', 'created_at']
        },
        'load_raw_products': {
            'table_name': 'raw_products',
            'csv_file': 'product.csv',
            'columns': ['product_id', 'product_name', 'category', 'price']
        },
        'load_raw_campaigns': {
            'table_name': 'raw_campaigns',
            'csv_file': 'marketing_campaign.csv',
            'columns': ['campaign_id', 'campaign_name', 'channel', 'start_date', 'end_date', 'budget']
        },
        'load_raw_orders': {
            'table_name': 'raw_orders',
            'csv_file': 'order.csv',
            'columns': ['order_id', 'user_id', 'product_id', 'order_date', 'quantity', 'total_amount']
        },
        'load_raw_clickstreams': {
            'table_name': 'raw_clickstreams',
            'csv_file': 'clickstream_logs.csv',
            'columns': ['event_time', 'user_id', 'session_id', 'page_url', 'device_type']
        }
    }

    operators = {}
    for task_id, config in tasks.items():
        operators[task_id] = PythonOperator(
            task_id=task_id,
            python_callable=load_csv_to_postgres,
            op_kwargs={**config, 'task_id': task_id, 'refresh_data': False}
        )

    [operators['load_raw_users'], operators['load_raw_products'], operators['load_raw_campaigns']] >> \
    operators['load_raw_orders']
    operators['load_raw_users'] >> operators['load_raw_clickstreams']