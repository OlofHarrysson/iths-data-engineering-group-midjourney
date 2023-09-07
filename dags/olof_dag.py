from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import download_blogs_from_rss
from newsfeed.dag_test_file_1 import function_1
from newsfeed.dag_test_file_2 import function_2


@task(task_id="function_1_task")
def function_1_task() -> None:
    function_1()


@task(task_id="function_2_task")
def function_2_task() -> None:
    function_2()


@task(task_id="download_blogs_from_rss_task")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main(blog_name="mit")


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    function_1_task() >> function_2_task() >> download_blogs_from_rss_task()


# register DAG
test_pipeline()
