from airflow import DAG
from airflow.operators.python import PythonOperator
from plugins.operators.custom_crawl_operator import CrawlCommentsOperator
from datetime import datetime
from src.config import output_crawl_file, post_url, MYSQL_DEFAULT

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

def clean_and_load_data(input_file, table_name):
    """Clean data and either save to CSV or load directly to Data Warehouse."""
    from src.cleaner.basic_cleaner import DataCleaner
    from src.loader.mysql_loader import MySQLLoader
    import csv

    cleaner = DataCleaner()
    cleaned_comments = []

    # Read and clean data
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_comment = cleaner.clean_comment(row["comment"])
            cleaned_comments.append({"comment": cleaned_comment})

        # Load to Data Warehouse
        loader = MySQLLoader(conn_id=MYSQL_DEFAULT)
        loader.load_to_mysql(data = cleaned_comments, table_name=table_name)
        print(f"Data loaded directly into table: {table_name}")


with DAG("facebook_comment_pipeline", default_args=default_args, schedule_interval="@daily") as dag:

    # Task 1: Crawl comments and save to CSV
    fetch_comments = CrawlCommentsOperator(
        task_id="fetch_comments",
        post_url= post_url,
        output_file=output_crawl_file
    )

    # Task 2: Clean comments from the CSV and load to Data Warehouse
    clean_and_load_data = PythonOperator(
        task_id="clean_and_load_data",
        python_callable=clean_and_load_data,
        provide_context=True,
        op_kwargs={
            "input_file": output_crawl_file,
            "table_name": "comments"
        }
    )

    fetch_comments >> clean_and_load_data
