# from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
# from google.cloud import bigquery
# import csv
# import os
#
# class BigQueryLoader:
#     def __init__(self, gcp_conn_id, project_id):
#         """
#         Initialize the BigQuery loader.
#         Args:
#             gcp_conn_id (str): Airflow connection ID for GCP.
#             project_id (str): GCP project ID.
#         """
#         self.gcp_conn_id = gcp_conn_id
#         self.project_id = project_id
#
#     def load_data_to_bigquery(self, data, dataset_id, table_id, write_disposition="WRITE_APPEND"):
#         """
#         Load in-memory data (list of dictionaries) into BigQuery.
#         Args:
#             data (list[dict]): List of rows (as dictionaries) to load into BigQuery.
#             dataset_id (str): BigQuery dataset ID.
#             table_id (str): BigQuery table ID.
#             write_disposition (str): BigQuery write disposition (e.g., WRITE_APPEND, WRITE_TRUNCATE).
#         """
#         bigquery_hook = BigQueryHook(gcp_conn_id=self.gcp_conn_id)
#         client = bigquery_hook.get_client()
#
#         # Convert data to rows and insert
#         table_ref = client.dataset(dataset_id).table(table_id)
#         errors = client.insert_rows_json(table_ref, data)  # Insert in-memory data
#
#         if errors:
#             raise RuntimeError(f"Encountered errors while inserting rows: {errors}")
#         print(f"Data successfully loaded into {dataset_id}.{table_id}")
