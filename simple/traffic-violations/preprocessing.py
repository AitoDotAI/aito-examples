from fuzzywuzzy import process
import json
from multiprocessing import cpu_count, Pool
import numpy
import pandas
import sys, getopt

def parallelize(data, func):
    cores = cpu_count() - 1 # use n-1 cores
    dataSplit = numpy.array_split(data, cores)
    pool = Pool(cores)
    data = pandas.concat(pool.map(func, dataSplit))
    pool.close()
    pool.join()
    return data

def carMakerToClass(dataSplit):
  def toClass(value):
    if value == 'VW':
      return 'VOLKSWAGEN'
    try:
      return process.extractOne(value, carMakers)[0]
    except TypeError:
      return 'NONE'
  
  return dataSplit.map(toClass)

def timeToDayTime(value):
  time = int(value.split(':')[0])
  if time < 6:
    return  'night'
  elif time >= 6 and time < 12:
    return  'morning'
  elif time >= 12 and time < 18:
    return  'day'
  else:
    return  'evening'

def preprocess(sampleSize=None):
  # Rename data columns
  data = pandas.read_csv('data/Traffic_Violations.csv',
    skiprows=1,
    names=[
      "date", "time", "agency", "subAgency", "description", "location", "latitude", "longitude", "accident", "belts", "injury", "damage",
      "fatal", "commercialLicence", "hazmat","commercialVehicle", "alcohol", "workZone", "state", "vehicleType", "vehicleYear", "vehicleMake", 
      "vehicleModel", "vehicleColor", "violation", "charge", "article", "contributed", "race", "gender", "driverCity", "driverState", "DLState", "arrestType", "geolocation"
    ])
  print('Data file read')
  
  # Sample the data
  if sampleSize:
    data = data.sample(sampleSize)
  
  # Drop unused columns
  data = data.dropna(subset=['vehicleYear'])
  data['vehicleYear'] = data['vehicleYear'].astype('int')
  data = data.drop(['date', 'location', 'latitude', 'longitude','charge', 'article', 'geolocation', 'agency', 'subAgency', 'state', 
    'vehicleModel', 'contributed', 'race', 'driverCity', 'driverState', 'DLState', 'arrestType', 'commercialVehicle',
    'workZone', 'commercialLicence', 'gender'], axis=1)
  print('Not used data dropped')

  # Map 'Yes'/'No' to true/false
  data = data.replace('No', False)
  data = data.replace('Yes', True)
  print('Data to use Boolean values')

  # Classify timestamps
  data['time'] = data['time'].map(timeToDayTime)
  print('Time converted')

  # Fix vehicke manufacturer names
  data['vehicleMake'] = parallelize(data['vehicleMake'], carMakerToClass)
  print('Car manufacturers fixed')

  data.to_json('data/preprocessed.json', lines=True, orient='records')
  print('Data preprocessed')


def main(argv):
  try:
    opts, args = getopt.getopt(argv, 'h:s:',['sample='])
  except getopt.GetoptError:
      print('preprocessing.py [-s sampleSize]')
      sys.exit(2)

  sampleSize = None
  for opt, arg in opts:
      if opt == '-h':
         print('preprocessing.py [-s sampleSize]')
         sys.exit()
      elif opt in ("-s", "--sample"):
        sampleSize = int(arg)
         
  with open('data/carMakers.json') as f:
    carMakers = json.load(f)['makers']
  preprocess(sampleSize)

if __name__ == "__main__":
   main(sys.argv[1:])

