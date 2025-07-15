from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 1),
}

with DAG('load_csv_to_postgres',
         schedule_interval=None,
         catchup=False,
         default_args=default_args) as dag:

    load_customer = BashOperator(
        task_id='load_customer',
        bash_command='psql postgresql://user:password@postgres:5432/dbname -c "\\copy dim_customer FROM \'/opt/airflow/dags/data/dim_customer.csv\' DELIMITER \',\' CSV HEADER;"'
    )

    load_product = BashOperator(
        task_id='load_product',
        bash_command='psql postgresql://user:password@postgres:5432/dbname -c "\\copy dim_product FROM \'/opt/airflow/dags/data/dim_product.csv\' DELIMITER \',\' CSV HEADER;"'
    )

    load_date = BashOperator(
        task_id='load_date',
        bash_command='psql postgresql://user:password@postgres:5432/dbname -c "\\copy dim_date FROM \'/opt/airflow/dags/data/dim_date.csv\' DELIMITER \',\' CSV HEADER;"'
    )

    load_fact = BashOperator(
        task_id='load_fact',
        bash_command='psql postgresql://user:password@postgres:5432/dbname -c "\\copy fact_order FROM \'/opt/airflow/dags/data/fact_order.csv\' DELIMITER \',\' CSV HEADER;"'
    )

    [load_customer, load_product, load_date] >> load_fact
