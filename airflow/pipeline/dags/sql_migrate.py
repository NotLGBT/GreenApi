from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Declare DAG 
dag = DAG(
    'json_to_mysql_etl',
    default_args=default_args,
    description='ETL DAG to extract data from JSON, transform, and load into MySQL',
    schedule_interval=None,  
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

SCRIPT_PATH = '/usr/local/airflow/scripts/extract.py'

#Run script 
def run_etl_script():
    return subprocess.run(['python3', SCRIPT_PATH], capture_output=True, text=True)

#Handle it with Operator
run_etl = PythonOperator(
    task_id='run_etl_script',
    python_callable=run_etl_script,
    dag=dag,
)
#Invokation 
run_etl
