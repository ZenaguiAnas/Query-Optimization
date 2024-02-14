
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# import os
# import sys

# script_dir = os.path.dirname(os.path.abspath(__file__))

# project_root = os.path.abspath(os.path.join(script_dir, '..'))
# sys.path.append(project_root)

# from src.data_preprocessing.preprocessing_script import data_preprocessing
# from src.train_model import train_model

def pre_processing():
    return "Pre-processing"

def training():
    return "Training"


default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='query_optimization_dag',
    start_date=datetime(2024, 1, 17, 5),
    default_args=default_args,
    description='DAG for Query Optimization.',
    schedule_interval='@daily'
) as dag:

    # Task 1: Preprocessing Task
    preprocessing_task = PythonOperator(
        task_id='preprocessing_task',
        python_callable=pre_processing,  
        provide_context=True,
        dag=dag,
    )

    # run_this = BashOperator(
    #     task_id="run_after_loop",
    #     bash_command="echo 1",
    # )

    # run_this_also = BashOperator(
    #     task_id="run_after_loop_2",
    #     bash_command="echo 2",
    # )

    # Task 2: Training Model Task
    training_task = PythonOperator(
        task_id='training_task',
        python_callable=training,  
        provide_context=True,
        dag=dag,
    )

    # run_this >> run_this_also
    preprocessing_task >> training_task
    # training_task