"""
This DAG is responsible for processing Workday data.
It performs X, Y, and Z steps in the workflow
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import boto3
import subprocess
import os

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define S3 bucket and paths
S3_BUCKET = "airflow-dags-production-bucket-new"
SCRIPTS_PATH = "scripts/pyspark/sample_script.py"
OUTPUT_PATH = "logs/output.txt"

# Helper function to download script from S3
def download_script_from_s3():
    s3 = boto3.client('s3')
    local_path = '/tmp/sample_script.py'
    s3.download_file(S3_BUCKET, SCRIPTS_PATH, local_path)
    return local_path

# Helper function to upload output to S3
def upload_output_to_s3():
    s3 = boto3.client('s3')
    local_output_path = '/tmp/output.txt'
    s3.upload_file(local_output_path, S3_BUCKET, OUTPUT_PATH)

# Task to execute the script
def execute_script():
    local_path = download_script_from_s3()
    subprocess.run(['python3', local_path], check=True)
    upload_output_to_s3()

# Define DAG
with DAG(
    'script_execution_dag',
    default_args=default_args,
    description='DAG to execute a script from S3 and store output back to S3',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['WORKDAY']
) as dag:

    # Task to execute script
    execute_script_task = PythonOperator(
        task_id='execute_script',
        python_callable=execute_script,
    )

    execute_script_task
