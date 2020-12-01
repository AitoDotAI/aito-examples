*** Settings ***
Documentation     A resource file with reusable keywords and variables for using Aito.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported AitoClient.
Library     aito.sdk.aito_client.AitoClient     %{AITO_INSTANCE_URL}     %{AITO_API_KEY}    False
Library     Collections

*** Keywords ***
Aito Predict
    [Arguments]    ${table}    ${inputs}    ${target}    ${limit}=1
    # table: String, name of the table in Aito schema
    # inputs: Dictionary, input data for prediction
    # target: String, name of the feature being predicted
    # limit: Integer, how many entries Aito returns

    # Ensure inputs are in correct format
    ${limit}=   Convert To Integer  ${limit}

    # Remove target feature from inputs if exists
    Remove From Dictionary      ${inputs}       ${target}

    # Construct predict query body as a Dictionary using arguments
    ${query}=       Create Dictionary   from=${table}   where=${inputs}   predict=${target}   limit=${limit}

    # Query from Aito
    ${response}=    Request              POST    /api/v1/_predict     ${query}

    # Return only first feature and probability
    [Return]  ${response['hits'][0]['feature']}  ${response['hits'][0]['$p']}

Aito Upload
    [Arguments]     ${table}        ${inputs}
    # table: String, name of the table in Aito schema
    # inputs: Dictionary, input data for prediction

    ${endpoint}=    Catenate    SEPARATOR=    /api/v1/data/       ${table}
    ${response}=    Request         POST        ${endpoint}   ${inputs}
    [Return]        ${response}

