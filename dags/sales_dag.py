from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from pipelines.load_sales_dw import run_load_sales_incremental, aggregate_daily_sales

default_args = {
    'owner': 'etl',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='sales_incremental',
    default_args=default_args,
    description='Incremental load for sales (runs every 30 minutes)',
    schedule_interval='*/30 * * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    load_incremental = PythonOperator(
        task_id='load_sales_incremental',
        python_callable=run_load_sales_incremental,
        op_kwargs={'chunk_size': 50000}
    )
