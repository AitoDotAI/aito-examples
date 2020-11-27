#!/usr/bin/python3

import pandas
from aito.schema import AitoTableSchema
from aito.client import AitoClient
from aito.api import delete_table, create_table, upload_entries
from aito.utils.data_frame_handler import DataFrameHandler

import os
import json

# 1. load the data
df = pandas.read_csv("../datasets/invoice-automation/invoice_data.csv")
print("loaded the invoice data.")

# 2. load schema
with open("schema.json") as f:
    schema = json.load(f)
print("wrote the invoice schema in schema.json.")

# 3. create the Aito table
aito_instance_url = os.environ.get('AITO_INSTANCE_URL')
aito_api_key = os.environ.get('AITO_API_KEY')

aito_client = AitoClient(instance_url=aito_instance_url, api_key=aito_api_key)
delete_table(client=aito_client, table_name='invoice_data')
create_table(client=aito_client, table_name='invoice_data', schema=schema)
print("created the aito database table.")

# 4. convert the dataframe to have correct type
entries = DataFrameHandler().convert_df_using_aito_table_schema(
  df=df,
  table_schema=schema
).to_dict(orient="records")
print("converted the dataframe.")

# 5. upload the entries
upload_entries(aito_client, table_name='invoice_data', entries=entries)
print("uploaded the entries.")
