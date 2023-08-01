import sys
import awswrangler as wr
from kestra import Kestra

# original file to ingest e.g. inbox/fruit_1.csv
INGEST_S3_KEY = sys.argv[1] or "inbox/fruit_1.csv"
BUCKET_NAME = "kestraio"
# e.g. s3://kestraio/archive/inbox/fruit_1.csv
INGEST_S3_KEY_FULL_PATH = f"s3://{BUCKET_NAME}/archive/{INGEST_S3_KEY}"

# Iceberg table
DATABASE = "default"
TABLE = "raw_fruits"

# Iceberg table's location
S3_PATH = f"s3://{BUCKET_NAME}/{TABLE}"
S3_PATH_TMP = f"{S3_PATH}_tmp"

MERGE_QUERY = """
MERGE INTO fruits f USING raw_fruits r
    ON f.fruit = r.fruit
    WHEN MATCHED
        THEN UPDATE
            SET id = r.id, berry = r.berry, update_timestamp = current_timestamp
    WHEN NOT MATCHED
        THEN INSERT (id, fruit, berry, update_timestamp)
              VALUES(r.id, r.fruit, r.berry, current_timestamp);
"""

df = wr.s3.read_csv(INGEST_S3_KEY_FULL_PATH)
nr_rows = df.id.nunique()
print(f"Ingesting {nr_rows} rows")
Kestra.counter("nr_rows", nr_rows, {"table": TABLE})

df = df[~df["fruit"].isin(["Blueberry", "Banana"])]
df = df.drop_duplicates(subset=["fruit"], ignore_index=True, keep="first")

wr.catalog.delete_table_if_exists(database=DATABASE, table=TABLE)

wr.athena.to_iceberg(
    df=df,
    database=DATABASE,
    table=TABLE,
    table_location=S3_PATH,
    temp_path=S3_PATH_TMP,
    partition_cols=["berry"],
    keep_files=False,
)

wr.athena.start_query_execution(
    sql=MERGE_QUERY,
    database=DATABASE,
    wait=True,
)
print(f"New data successfully ingested into {S3_PATH}")