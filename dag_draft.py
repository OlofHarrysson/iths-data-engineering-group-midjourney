from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _print_message():
    print(f"Executing task")


with DAG(
    dag_id="blog_DAG", start_date=datetime(2023, 9, 5), schedule_interval="@daily", catchup=False
):
    execute_task_1 = PythonOperator(task_id="print_at_step_1", python_callable=_print_message)
    execute_task_2 = PythonOperator(task_id="print_at_step_2", python_callable=_print_message)

(execute_task_1 >> execute_task_2)
