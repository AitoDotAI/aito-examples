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
# 1. Setup the Aito Client
#

aito_instance_url = os.environ.get('AITO_INSTANCE_URL')
aito_api_key = os.environ.get('AITO_API_KEY')

db = AitoClient(instance_url=aito_instance_url, api_key=aito_api_key)

#
# 2. Setup infrastructure for browser & dialogs
#
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://anttiaito.wufoo.com/forms/z1gfzm4o11v5ekc/")

parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one


#
# 3. Wait for the Item Description to be filled, and read the value
#

info = messagebox.showinfo('Instructions', "Fill the item description with e.g. 'Real estate rent. Deltona corp' and click OK. Robot will fill the rest as it is able.", parent=parent)

input = driver.find_element_by_name("Field1")
description = input.get_attribute('value')

#
# 4. Use Aito to predict the missing values and fill the form
#

def fill_field(field_title, field_element, field_name, item_description):
    hits = \
      predict(db, {
          "from": "invoice_data",
          "where" : {
              "Item_Description": item_description
          },
          "predict" : field_name
      })["hits"]
    p = hits[0]["$p"]
    prediction = hits[0]["feature"]
    if p >= 0.1:
        field = driver.find_element_by_name(field_element)
        field.send_keys(prediction)
        if p <= 0.98:
            info = messagebox.showinfo('Please review!', f"Review {field_title}! Confidence is only {int(p*100)}%", parent=parent)
   
fill_field("Product category", "Field2", "Product_Category", description)
fill_field("GL code", "Field3", "GL_Code", description)
fill_field("Vendor code", "Field4", "Vendor_Code", description)

#
# 5. Ask, if the invoice should be uploaded to Aito. If so, upload it.
#

teach = messagebox.askquestion ('Teach Aito?','Would you like to upload this invoice to Aito?', parent=parent)

def read_field(field_element):
    return driver.find_element_by_name(field_element).get_attribute('value')

if teach == 'yes':
    # Figure out the next invoice id
    inv_id = \
      search(db, {
          "from": "invoice_data",
          "orderBy" : "Inv_Id"
      })["hits"][0]["Inv_Id"]+1
    # This is the new invoice entry
    entry = {
        "Item_Description" : read_field("Field1"),
        "Product_Category" : read_field("Field2"),
        "GL_Code" : read_field("Field3"),
        "Vendor_Code" : read_field("Field4"),
        "Inv_Amt": 1,
        "Inv_Id": inv_id
    }
    # upload the data and inform the user, it's done
    upload_entries(db, table_name='invoice_data', entries=[entry])
    messagebox.showinfo('Done.', f"Inventory item {inv_id} was added.", parent=parent)



