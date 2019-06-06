#!/bin/bash

set -e
set -x

echo -e "Downloading upload-file.sh .."
curl -O https://raw.githubusercontent.com/AitoDotAI/aito-tools/4696ff0c198d84cfe2e69690ead9b1aaff346a2b/upload-file.sh

echo -e "Resetting aito database .."

AITO_URL=https://$AITO_ENV.api.aito.ai

# Delete contents
curl -sS -H "x-api-key: $API_KEY" -X DELETE "$AITO_URL/api/v1/schema"

# Create schema
curl -sS -H "x-api-key: $API_KEY" -H "content-type: application/json" -d@schema.json -X PUT "$AITO_URL/api/v1/schema"

jq -c '.[]' products.json > products.ndjson
jq -c '.[]' users.json > users.ndjson
jq -c '.[]' orders.json > orders.ndjson
jq -c '.[]' invoices.json > invoices.ndjson
jq -c '.[]' impressions.json > impressions.ndjson

bash ./upload-file.sh products.ndjson $AITO_URL
bash ./upload-file.sh users.ndjson $AITO_URL
bash ./upload-file.sh orders.ndjson $AITO_URL
bash ./upload-file.sh invoices.ndjson $AITO_URL
bash ./upload-file.sh impressions.ndjson $AITO_URL
