from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# Function to be executed by PythonOperator
def print_hello():
    print("Hello, Airflow!")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'wd_dag1',
    default_args=default_args,
    description='A simple sample DAG',
    schedule_interval=timedelta(days=1),  # Runs once a day
)

dag_tags = [
    'business_domain:WORKDAY'
]

# Define the tasks
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set task dependencies
start_task >> hello_task >> end_task
