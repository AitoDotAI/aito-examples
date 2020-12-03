#!/usr/bin/python3

#
# 1. Import libraries, open the client
#
from aito.client import AitoClient
from aito.api import evaluate
import os

db = AitoClient(os.environ.get('AITO_INSTANCE_URL'),
                os.environ.get('AITO_API_KEY'))

#
# 2. Define a method, that estimate KPIs for a field
#
def evaluate_field(field_name):
    # a) Execute the evaluation query to get the individual predictions.
    #    Note that the query inside 'evaluate' field must match the robot's query
    cases = \
        evaluate(db, {
            "test": {
                "$index": { "$mod": [10, 0] }
            },
            "evaluate": {
                "from": "invoices",
                "where": {
                    "Item_Description": {"$get": "Item_Description"},
                },
                "predict": field_name
            },
            "select": ["cases"]
        })["cases"]
    n = len(cases)
    
    # b) Print some general information and CSV headers
    print()
    print(f"KPIs by confidence for {field_name} based on {n} predictions")
    print()
    print("confidence, fill rate, error, reviewed €, automated €")    

    # a) Measure fill rates, errors and business value for each confidence threshold
    for confidence in [0.05, 0.1, 0.25, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99]:
        errors = 0
        filled = 0
        for case in cases:
            # count only predictions above the minimum confidence threshold
            if case["top"]["$p"] >= confidence:
                filled += 1
                if case["accurate"] == False:
                    errors += 1

        # with review, assume each correctly filled field to save 0.5€ and each error cost 0.1€
        reviewed_value = 0.5 * (filled / n) + -0.1 * (errors / n)
        # without review, assume each correctly filled field to save 2€ and each error cost 40€
        automated_value = 2 * (filled / n) + -40 * (errors / n)
        print(f"{confidence}, {filled/n:.3f}, {errors/filled:.3f}, {reviewed_value:.3f}, {automated_value:.3f}")
    print()

#
# 3. Run evaluations for the 3 predicted fields
#
evaluate_field("Product_Category")
evaluate_field("GL_Code")
evaluate_field("Vendor_Code")
