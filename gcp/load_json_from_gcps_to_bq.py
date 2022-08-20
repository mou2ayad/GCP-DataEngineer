from google.cloud import bigquery

crd_file='/Users/mouayadkhashfeh/Downloads/zeta-period-359422-95e8368cd3ce.json'
# Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(crd_file)

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "zeta-period-359422.bq_dataeng_assignment.yc_app_events"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("uuid", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("data", "JSON", mode="NULLABLE"),
        bigquery.SchemaField("meta", "JSON", mode="NULLABLE"),
        bigquery.SchemaField("type", "STRING", mode="REQUIRED"),
    ]
)

uri = "gs://yc-learning/yc-test/yc_app_events_2022_05_31.json"

load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="EU", 
    job_config=job_config,
)  

load_job.result()  

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))