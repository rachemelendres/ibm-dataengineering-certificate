# import the libraries

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Rache M',
    'start_date': days_ago(0),
    'email': ['rache@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='ETL Pipeline for Processing Web Server Log Files',
    schedule_interval=timedelta(days=1),
)

# define the tasks

PATH='/home/project/airflow/dags/capstone/'
# define the first task

extract_data = BashOperator(
    task_id='extract_data',
    bash_command=f"cut -f1 -d' ' '{PATH}'/accesslog.txt > '{PATH}'/extracted_data.txt",
    dag=dag,
)

# define the second task

transform_data = BashOperator(
    task_id='transform_data',
    bash_command=f"grep -v '198.46.149.143' '{PATH}'/extracted_data.txt > '{PATH}'/transformed_data.txt",
    dag=dag,
)

# define the last task
load_data = BashOperator(
    task_id='load_data',
    bash_command=f"tar -cvf '{PATH}'/weblog.tar '{PATH}'/transformed_data.txt",
    dag=dag,
)
# task pipeline
extract_data >> transform_data >> load_data