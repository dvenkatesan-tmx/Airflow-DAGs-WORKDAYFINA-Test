"""
This DAG is responsible for processing Workday data.
It performs X, Y, and Z steps in the workflow.
"""

from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
import boto3

# S3 Bucket and Object details
S3_BUCKET = 'airflow-dags-production-bucket-new'
SCRIPTS_PATH = 'scripts/pyspark/sample_script.py'  
OUTPUT_PATH = 'logs/output_script.py'


def download_and_upload_script():
    """
    Downloads a script from S3 and uploads it back to a different location in the same bucket.
    """
    s3 = boto3.client('s3')

    # Define in-memory file paths for downloading and uploading
    local_file = 'sample_script.py'
    output_local_file = 'output_script.py'

    # Download the script from S3
    print(f"Downloading from S3://{S3_BUCKET}/{SCRIPTS_PATH} to {local_file}")
    s3.download_file(S3_BUCKET, SCRIPTS_PATH, local_file)

    print(f"Copying {local_file} to {output_local_file}")
    with open(local_file, 'rb') as f:
        with open(output_local_file, 'wb') as out_f:
            out_f.write(f.read())

    # Upload the output file back to S3
    print(f"Uploading {output_local_file} to S3://{S3_BUCKET}/{OUTPUT_PATH}")
    s3.upload_file(output_local_file, S3_BUCKET, OUTPUT_PATH)

    # Return the file paths for debugging purposes
    return output_local_file


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 18),
}


with DAG(
    'wd_dag1',
    default_args=default_args,
    description='Workday DAG for testing script download and upload',
    schedule_interval=timedelta(days=1),
    tags=['WORKDAY']
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    download_and_upload_task = PythonOperator(
        task_id='download_and_upload_script',
        python_callable=download_and_upload_script
    )

    start >> download_and_upload_task
