# Finding statistical relationships within traffic violations

How to duplicate traffic violations demo

## Downloading the data

Data used in this example is [traffic violations data from Maryland](https://catalog.data.gov/dataset/traffic-violations-56dda).

## Preprocessing

As the data contains a lot of information, we removed some columns to make this example simpler and more easily understandable. We also classified timestamps into four classes:

- night
- morning
- day
- evening

Each class is a six hour period.

We noticed that the vehicle manufacturers column contained a lot of abbreviations and slang names for different manufacturers and therefore we used [edit distance](https://en.wikipedia.org/wiki/Edit_distance) to find the closest manufacturer.

Code of the preprocessing can be found from [preprocessing.py](/preprocessing.py). We used [Pipenv](https://github.com/pypa/pipenv) to manage the packages of the preprocessing. From [Pipfile](/Pipfile) you can find all requirements and use your favourite package manager.

## Creating the schema

Before uploading the data we need to define schema. We can use the same data model defined in the preprocessing phase:

```javascript
{
  "schema": {
    "violations": {
      "type": "table",
      "columns": {
        "accident": { "type": "Boolean" },
        "alcohol": { "type": "Boolean" },
        "belts": { "type": "Boolean" },
        "description": { "type": "String" },
        "fatal": { "type": "Boolean" },
        "hazmat": { "type": "Boolean" },
        "injury": { "type": "Boolean" },
        "damage": { "type": "Boolean" },
        "time": { "type": "String" },
        "vehicleColor": { "type": "String", "nullable": true },
        "vehicleMake": { "type": "String", "nullable": true },
        "vehicleType": { "type": "String" },
        "vehicleYear": { "type": "Int"},
        "violation": { "type": "String" }
      }
    }
  }
}
```

More about schema creation you can read from [our API documentation](https://aito.ai/docs/api/#put-api-v1-schema).

## Uploading the data

Before uploading the data to Aito, we need to gzip the preprocessed data file. This can be done easily with command line:

```bash
gzip preprocessed.json
```

After gzipping the data can be uploaded to Aito. We used [uploadData.py](/uploadData.py) file for this. More about file upload you can read from [our API documentation](https://aito.ai/docs/api/#post-api-v1-data-table-file)

## Querying from Aito

After all lines have been uploaded, we can start using Aito.
For example the query used in [traffic violations example](https://aito.ai/example-gallery/traffic-violations)
used the [predict endpoint](https://aito.ai/docs/api/#post-api-v1-predict) for predicting the time of the traffic violations:

```javascript
{
  "select": [
    "feature",
    "$p"
  ],
  "from": "violations",
  "where": {
    "violation": "Warning",
    "vehicleMake": "VOLVO",
    "vehicleColor": "BLACK"
  },
  "predict": "time",
  "exclusiveness": true
}
```
