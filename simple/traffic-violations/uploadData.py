import requests

aitoUrl = 'AITO_URL' + '/data/violations/file'
dataPath = 'PATH_TOGZIPPED_DATA'
apiKey = 'READ_WRITE_API_KEY'

headers = {'x-api-key': apiKey, 'Content-Type': 'application/json'}
fileAPIResponse = requests.post(aitoUrl, headers=headers)
response = fileAPIResponse.json()

url = response['url']
fileApiId = response['id']

with open(dataPath, 'rb') as data:
  requests.put(url, data=data)

triggerUrl =  aitoUrl +  '/' + fileApiId
trigger = requests.post(triggerUrl, headers=headers)
print(trigger.json())

