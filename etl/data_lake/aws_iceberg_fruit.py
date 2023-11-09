import sys
import awswrangler as wr
from kestra import Kestra

# original file to ingest e.g. s3://kestraio/inbox/
INGEST_S3_KEY_PATH = "s3://kestraio/archive/inbox/"

if len(sys.argv) > 1:
    INGEST_S3_KEY_PATH = sys.argv[1]
else:
    print(f"No custom path provided. Using the default path: {INGEST_S3_KEY_PATH}.")

# Iceberg table
BUCKET_NAME = "kestraio"
DATABASE = "default"
TABLE = "raw_fruits"

# Iceberg table's location
S3_PATH = f"s3://{BUCKET_NAME}/{TABLE}"
S3_PATH_TMP = f"{S3_PATH}_tmp"

if not INGEST_S3_KEY_PATH.startswith("s3://"):
    INGEST_S3_KEY_PATH = f"s3://{BUCKET_NAME}/{INGEST_S3_KEY_PATH}"

df = wr.s3.read_csv(INGEST_S3_KEY_PATH)
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
print(f"New data successfully ingested into {S3_PATH}")
