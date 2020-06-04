from fuzzywuzzy import process
import json
from multiprocessing import cpu_count, Pool
import numpy
import pandas
import argparse

def parallelize(data, func):
    cores = cpu_count() - 1 # use n-1 cores
    dataSplit = numpy.array_split(data, cores)
    pool = Pool(cores)
    data = pandas.concat(pool.map(func, dataSplit))
    pool.close()
    pool.join()
    return data

def carMakerToClass(dataSplit):

  with open('data/vehicleManufacturers.json') as f:
    carMakers = json.load(f)['makers']

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

def preprocess(dataPath, sampleSize=None):
  # Rename data columns
  data = pandas.read_csv(dataPath,
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


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dataPath')
  parser.add_argument('-s', '--sample', help='Sample data', nargs='?', const=1000, type=int)
  args = parser.parse_args()
  preprocess(args.dataPath, args.sample)

if __name__ == "__main__":
   main()

