#!/usr/bin/python3

# import for browser automation
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# aito DB imports
from aito.client import AitoClient
from aito.api import search, predict, search, upload_entries

# for dialog
import tkinter
from tkinter import messagebox

# for reading env values
import os

#
# 1. Set up the aito, the browser and the dialogue infrastructure
#

db = AitoClient(os.environ.get('AITO_INSTANCE_URL'),
                os.environ.get('AITO_API_KEY'))

driver = webdriver.Chrome(ChromeDriverManager().install())

parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

#
# 2. Wait for the Item Description to be filled, and read the value
#

driver.get("https://anttiaito.wufoo.com/forms/z1gfzm4o11v5ekc/")
info = messagebox.showinfo('Instructions', "Fill the item description with e.g. 'Real estate rent. Deltona corp' and click OK. Robot will fill the rest as it is able.", parent=parent)

input = driver.find_element_by_name("Field1")
description = input.get_attribute('value')

#
# 3. Use Aito to predict the missing values and fill the form
#

def fill_field(field_title, field_element, field_name, item_description):
    # a) do the prediction and extract the hits
    hits = \
      predict(db, {
          "from": "invoices",
          "where" : {
              "Item_Description": item_description
          },
          "predict" : field_name
      })["hits"]
    # b) read the confidence level and the feature
    p = hits[0]["$p"]
    prediction = hits[0]["feature"]
    # c) if confidence is more than 0.1...
    if p >= 0.1:
        #...fill the field...
        field = driver.find_element_by_name(field_element)
        field.send_keys(prediction)
        #...and possibly request the user to review the content
        if p <= 0.98:
            message = f"Review {field_title}! Confidence is only {int(p*100)}%"
            info = messagebox.showinfo('Please review!', message, parent=parent)
   
fill_field("Product category", "Field2", "Product_Category", description)
fill_field("GL code", "Field3", "GL_Code", description)
fill_field("Vendor code", "Field4", "Vendor_Code", description)

#
# 4. Ask, if the invoice should be uploaded to Aito. If so, upload it.
#

teach = messagebox.askquestion (
    'Teach Aito?',
    'Would you like to upload this invoice to Aito?',
    parent=parent)

if teach == 'yes':
    # a) Figure out the next invoice id
    inv_id = \
      search(db, {
          "from": "invoices",
          "orderBy" : "Inv_Id"
      })["hits"][0]["Inv_Id"]+1
    # b) create the new invoice entry based on the form data
    def read_field(field_element):
        return driver.find_element_by_name(field_element).get_attribute('value')
    entry = {
        "Item_Description" : read_field("Field1"),
        "Product_Category" : read_field("Field2"),
        "GL_Code" : read_field("Field3"),
        "Vendor_Code" : read_field("Field4"),
        "Inv_Amt": 1,
        "Inv_Id": inv_id
    }
    # c) upload the data and inform the user, it's done
    upload_entries(db, table_name='invoices', entries=[entry])
    messagebox.showinfo('Done.', f"Invoice {inv_id} was successfully uploaded.", parent=parent)



