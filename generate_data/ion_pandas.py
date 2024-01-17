import amazon.ion.simpleion as ion
from amazon.ion.simple_types import IonPyNull
import pandas as pd
import requests


def convert_ion_nulls(value):
    return None if isinstance(value, IonPyNull) else value


url = "https://huggingface.co/datasets/kestra/datasets/resolve/main/ion/employees.ion"
response = requests.get(url)
response.raise_for_status()
ion_content = response.content
ion_data = ion.loads(ion_content, single_value=False)
list_of_dicts = [dict(record) for record in ion_data]
list_of_dicts = [
    {k: convert_ion_nulls(v) for k, v in record.items()} for record in list_of_dicts
]
df = pd.DataFrame(list_of_dicts)
