import requests
import polars as pl
import amazon.ion.simpleion as ion
from amazon.ion.simple_types import IonPyDecimal, IonPyNull


def convert_ion_types(value):
    if isinstance(value, IonPyNull):
        return None
    elif isinstance(value, IonPyDecimal):
        return float(value)
    else:
        return value


url = "https://huggingface.co/datasets/kestra/datasets/resolve/main/ion/employees.ion"
response = requests.get(url)
response.raise_for_status()
ion_content = response.content
ion_data = ion.loads(ion_content, single_value=False)
list_of_dicts = [dict(record) for record in ion_data]
list_of_dicts = [
    {k: convert_ion_types(v) for k, v in record.items()} for record in list_of_dicts
]

polars_df = pl.DataFrame(list_of_dicts)
print(polars_df.glimpse())

import polars as pl
df = pl.read_ion("/path/to/file.ion")

polars_df.to_dict()