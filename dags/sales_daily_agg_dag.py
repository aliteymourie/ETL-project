from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from pipelines.load_sales_dw import aggregate_daily_sales

default_args = {
    'owner': 'etl',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='sales_daily_aggregation',
    default_args=default_args,
    description='Nightly aggregation of daily sales',
    schedule_interval='5 0 * * *',  # 00:05 daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    daily_agg = PythonOperator(
        task_id='daily_aggregate',
        python_callable=aggregate_daily_sales,
    )
