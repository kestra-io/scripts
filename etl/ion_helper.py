import polars as pl
import amazon.ion.simpleion as ion
from amazon.ion.simple_types import IonPyDecimal, IonPyNull

def read_ion(file_path):
    with open(file_path, 'rb') as f:
        ion_content = f.read()
    ion_data = ion.loads(ion_content, single_value=False)
    list_of_dicts = [{k: convert_ion_types(v) for k, v in dict(record).items()} for record in ion_data]
    return pl.DataFrame(list_of_dicts)

def write_ion(df, file_name):
    list_of_values = df.to_dict()
    with open(file_name, "wb") as f:
        ion.dump(list_of_values, f)

def convert_ion_types(value):
    if isinstance(value, IonPyNull):
        return None
    elif isinstance(value, IonPyDecimal):
        return float(value)
    else:
        return value


import amazon.ion.simpleion as ion
from amazon.ion.simple_types import IonPyNull

def read_ion_to_dicts(file_path):
    with open(file_path, 'rb') as f:
        ion_content = f.read()
    ion_data = ion.loads(ion_content, single_value=False)
    return [{k: convert_ion_nulls(v) for k, v in dict(record).items()} for record in ion_data]

def write_dicts_to_ion(dict_or_list, file_name):
    with open(file_name, "wb") as f:
        ion.dump(dict_or_list, f)

def convert_ion_nulls(value):
    return None if isinstance(value, IonPyNull) else value
