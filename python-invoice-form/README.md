# Aito Python / Selenium invoice form filling demo

This demo contains a simple attended bot, which opens an invoice form in a browser, requests user to
input item description, and then fills the remaining fields based on Aito predictions. After the
operation, the robot asks from the user, whether the invoice should be uploaded to Aito. If it is,
the invoice is inserted to the database.

This robot is very similar to the robotframework robot. It's main difference is that
it's written with Python and Selenium instead of Robot Framework.

# How to run?

First do the necessary preparations:

```
pipenv install
pipenv shell
```

Next, you can prepare the database with:

```
AITO_INSTANCE_URL=<YOU_HOST_URL> AITO_API_KEY=<YOUR_API_KEY> ./prepare.py
```

And run the robot with

```
AITO_INSTANCE_URL=<YOU_HOST_URL> AITO_API_KEY=<YOUR_API_KEY> ./robot.py
```

Alternatively, you can run the robot against the public-1 database:

```
AITO_INSTANCE_URL=https://public-1.api.aito.ai AITO_API_KEY=bvss2i2dIkaWUfBCdzEO89LpxUkwO3A24hYg8MBq ./robot.py
```

NOTE that the robot cannot add more data to the public-1 database, because it lacks the read write key. If you try to add data using the robot, it will fail with an exception.

# How to use the robot?

After starting the robot, it will open a browser with an invoice form in it, and open a dialog
with 'OK' button and a message about 'filling the item description'.

Next: write e.g. 'real estate rent, deltona corp' to the item description field.

Then click the 'OK' button and the robot will fill the invoice form with GL_Code, Product_Category and Vendor_Code predictions. Robot will warn about the low confidence predictions.

As the last step, robot will ask you whether the filled invoice should be added to Aito.
If you ask 'yes', the Robot will upload filled invoice to the Aito database.