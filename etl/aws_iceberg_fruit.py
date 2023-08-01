import glob
import sys

import awswrangler as wr
from kestra import Kestra
import pandas as pd

BUCKET_NAME = "kestraio"
DATABASE = "default"
TABLE = "raw_fruits"
SOURCE_FILES = "fruit_*.csv"
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


def extract_from_source_system() -> pd.DataFrame:
    files_list = glob.glob(SOURCE_FILES)
    if not files_list:
        sys.exit(f"No new files to process.")
    fruits_df = pd.concat(map(pd.read_csv, files_list))
    nr_rows = fruits_df.id.nunique()
    print(f"Ingesting {nr_rows} rows")
    Kestra.counter("nr_rows", nr_rows, {"table": TABLE})
    return fruits_df


df = extract_from_source_system()
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
