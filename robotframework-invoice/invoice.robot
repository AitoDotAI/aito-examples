*** Settings ***
Documentation     Invoice categorization with Aito.
...
Library     OperatingSystem
Resource    aitohelper.robot

*** Variables ***
${table}=       invoice_data        # Name of table in Aito insance
${target}=      Product_Category    # Name of the feature we want to predict
${path}=        ./files
${pathCate}=    ./files/categorized

*** Test Cases ***

Categorize Invoices
    # Loop through all files in directory
    ${files}=                   List Files In Directory     ${path}
    FOR     ${fileName}         IN              @{files}
        
        # Read file
        ${filePath}=            Join Path       ${path}     ${fileName}
        ${data}=                Get File        ${filePath}

        # Turn file content into a dictionary and check if target exists in dictionary
        ${data}=                Evaluate        ${data}
        ${exists}=              Evaluate        '${target}' in ${data}                 

        # If target does not exist in dictionary, predict the most probable value
        ${pred}   ${prob} =     Run Keyword Unless              ${exists}     Aito Predict      ${table}    ${data}      ${target}
        
        # If target exists in dictionary and no need to predict, upload dictionary into Aito
        Run Keyword If          ${exists}     Aito Upload       ${table}    ${data}
        
        # If prediction was made, add predicted value to dictionary
        Run Keyword Unless      ${exists}     Set To Dictionary    ${data}    ${target}   ${pred}
 
        # Convert dictionary to string and write into a file
        ${data}=                Convert To String   ${data}
        ${filePath}=            Join Path       ${pathCate}    ${fileName}
        Create File             ${filePath}     ${data}
    END
