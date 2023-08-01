import sys

import awswrangler as wr
from kestra import Kestra
import pandas as pd


FILE = sys.argv[1] or "{{taskrun.value}}"
BUCKET_NAME = "kestraio"
DATABASE = "default"
TABLE = "raw_fruits"
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


def extract_from_source_system(file: str = FILE) -> pd.DataFrame:
    fruits_df = pd.read_csv(file)
    nr_rows = fruits_df.id.nunique()
    print(f"Ingesting {nr_rows} rows")
    Kestra.counter("nr_rows", nr_rows, {"table": TABLE})
    return fruits_df


df, nr_rows = extract_from_source_system()
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
