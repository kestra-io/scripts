import requests
import boto3
from kestra import Kestra

BUCKET = "kestraio"


def extract_and_upload(file):
    url = f"https://raw.githubusercontent.com/kestra-io/datasets/main/{file}"

    response = requests.get(url)
    data = response.content.decode("utf-8")
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET).put_object(Key=file, Body=data)
    print(f"{url} downloaded and saved to {BUCKET}/{file}")


for month in range(1, 13):
    filename = f"monthly_orders/2023_{str(month).zfill(2)}.csv"
    extract_and_upload(filename)
    Kestra.outputs({f"{filename}": f"s3://{BUCKET}/{filename}"})
