from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import (
    download_blogs_from_rss,
    extract_articles,
    summarize,
    translation_model,
)

blogs_list = [
    "mit",
    "ai_blog",
]  # TODO: add google_ai #TODO: and open_ai if model "api" is to be used


@task(task_id="download_blogs")
def download_blogs_from_rss_task() -> None:
    for blog in blogs_list:
        download_blogs_from_rss.main(blog_name=blog)


@task(task_id="extract_blogs")
def extract_blogs_task() -> None:
    for blog in blogs_list:
        extract_articles.main(blog_name=blog)


@task(task_id="summarize_blogs")
def summarize_blogs_task() -> None:
    for blog in blogs_list:
        summarize.main(blog_name=blog, model_type="api")  # run local_model if api out of money


@task(task_id="translate_blogs")
def translate_blogs_task() -> None:
    for blog in blogs_list:
        translation_model.main(blog_name=blog)


@dag(
    dag_id="dashboard_pipline",
    start_date=datetime(2023, 6, 2),
    schedule_interval="@daily",  # TODO: change to "*/5 * * * *" when pipeline is working
    catchup=False,
)
def pipeline():
    (
        download_blogs_from_rss_task()
        >> extract_blogs_task()
        >> summarize_blogs_task()
        >> translate_blogs_task()
    )


# Register the DAG
pipeline_instance = pipeline()
