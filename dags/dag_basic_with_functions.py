import sys
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(Path(__file__).parent / "src")

from newsfeed.dag_test_file_1 import function_1
from newsfeed.dag_test_file_2 import function_2

with DAG(dag_id="blog_DAG_with_functions", start_date=datetime(2023, 9, 5)):
    execute_task_1 = PythonOperator(task_id="print_from_function_1", python_callable=function_1)
    execute_task_2 = PythonOperator(task_id="print_from_function_2", python_callable=function_2)

(execute_task_1 >> execute_task_2)
