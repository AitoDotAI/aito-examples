# Aito Robot Framework invoice form filling demo

This demo contains a simple attended bot, which opens an invoice form in a browser, requests user to input item description, and then fills the remaining fields based on Aito predictions.

![The intelligent invoice form filling robot in action](resources/invoice-form.gif?raw=true "Robot framework bot fill missing fields, once you input the 'Item Description' field")

## How does it work?

aito-rf-invoice-demo bot uses a public invoice data set from the public 'public-1' [Aito](https://aito.ai) database instance. The database instance provides the capacity to predict any field from any table based on any arbitrary 'known information'.

In practice the robot uses the following kinds of predictive queries to predict the missing fields:

```json
{
  "from": "invoice_data",
  "where": {
    "Item_Description": "real estate rents deltona corp"
  },
  "predict": "Product_Category",
  "limit" : 1
}
```

The predictions can be done in the Robot Framework with the following kind of code:

```
    # Construct predict query body as a Dictionary using arguments
    ${query}=       Create Dictionary   from=${table}   where=${inputs}   predict=${target}   limit=${limit}

    # Query for Aito
    ${response}    Predict      ${client}   ${query}
```

The source code is available [here](aito-invoice-demo.robot)

## How to setup?

Run the following commands to install the dependencies.

```
pip3 install aitoai==0.4.0
pip3 install robotframework==3.2.2
pip3 install robotframework-seleniumlibrary
pip3 install webdrivermanager
webdrivermanager firefox chrome --linkpath /usr/local/bin
```

## How to run?

Then start the robot with:

```bash
AITO_INSTANCE_URL=https://public-1.api.aito.ai AITO_API_KEY=bvss2i2dIkaWUfBCdzEO89LpxUkwO3A24hYg8MBq robot aito-invoice-demo.robot
```

The robot will open a browser with an invoice form in it, and open
a dialog with 'OK' button and a message about 'filling the item description'.

![Empty invoice form](resources/invoice-form-1.png?raw=true "Empty invoice form")

Next input the item description with e.g. 'real estate rent deltona corp'

![Item description filled](resources/invoice-form-2.png?raw=true "Invoice form with the item description filled")

Then click the 'OK' button and the robot will fill the invoice form with GL_Code, Product_Category and Vendor_Code predictions. Robot will warn about the low confidence predictions.

![Missing fields filled](resources/invoice-form-3.png?raw=true "Invoice form with the predictions filled")

