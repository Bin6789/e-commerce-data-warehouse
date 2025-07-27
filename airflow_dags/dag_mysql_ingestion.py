from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import sqlalchemy

default_args = {
    'start_date': datetime(2025, 1, 1),
}

CSV_DIR = '/opt/airflow/datasets/csv_for_mysql'
MYSQL_CONN = "mysql+pymysql://airflow:airflow@mysql:3306/ecommerce"

tables = {
    "users": "users.csv",
    "addresses": "addresses.csv",
    "categories": "categories.csv",
    "vendors": "vendors.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv"
}

def load_table(table_name, csv_file):
    df = pd.read_csv(f"{CSV_DIR}/{csv_file}")
    engine = sqlalchemy.create_engine(MYSQL_CONN)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"✅ Loaded {csv_file} to MySQL table {table_name}")

with DAG("dag_mysql_ingestion",
         default_args=default_args,
         schedule_interval=None,
         catchup=False,
         tags=['mysql', 'ingestion'],
         description="Ingest test data into MySQL"
         ) as dag:

    for tbl, csv in tables.items():
        task = PythonOperator(
            task_id=f"load_{tbl}",
            python_callable=load_table,
            op_kwargs={'table_name': tbl, 'csv_file': csv}
        )
