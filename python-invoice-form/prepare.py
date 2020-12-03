#!/usr/bin/python3
from aito.client import AitoClient
from aito.api import delete_table, create_table, upload_entries

import os, json, pandas

# 1. open the Aito client
db = AitoClient(os.environ.get('AITO_INSTANCE_URL'),
                os.environ.get('AITO_API_KEY'))

# 2. load the database schema and create the Aito table
delete_table(db, 'invoices')
with open("schema.json") as f:
    create_table(db, 'invoices', json.load(f))

# 3. upload the data
data_path = "../datasets/invoice-automation/invoice_data.csv"
upload_entries(db, 'invoices', pandas.read_csv(data_path).to_dict(orient="records"))
print("'invoices' table ready.")
