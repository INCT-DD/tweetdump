# IMPORT MODULES

from bson import json_util
import twint
import contextlib
import pymongo
import sys

# MONGODB AUTH DATA
mongoUser = ""  
mongoPasswd = ""
mongoHost = "127.0.0.1"
mongoPort = "27017"

# CREATE THE SEARCH PARAMETERS OBJECT

searchParameters = twint.Config()

# SET SEARCH PARAMETERS (referTo: https://github.com/twintproject/twint/wiki/Module)

searchParameters.Output = "tweets.json"
searchParameters.Search = "EleNao"
searchParameters.Since = "2018-10-01"
#searchParameters.Until = "2018-08-01"
searchParameters.Stats = True
searchParameters.Store_json = True
searchParameters.Profile_full = True
searchLog = "log.txt"

# RUN TWITTER SEARCH

print("Running search...")

with open(searchLog,'a') as f:
    with contextlib.redirect_stdout(f):
        twint.run.Search(searchParameters)

print("Search finished.")

# BUILD MONGO URL AND CONNECT TO DATABASE

mongoUrl = ''.join(["mongodb://", mongoUser, ":", mongoPasswd, "@", mongoHost, ":", mongoPort])

try:
  mongoConnection = pymongo.MongoClient(mongoUrl)
  insertDatabase = mongoConnection[searchParameters.Search]
  insertCollection = insertDatabase['tweets']
except: 
  print("CONNECTION ERROR. PLEASE CHECK YOUR DATABASE URL")
  sys.exit(1)
  
# LOAD THE DATA FILE

print("Loading data file to memory...")

with open(searchParameters.Output, 'r') as dataFile:
    dataStream = [json_util.loads(line) for line in dataFile]

print("Loading finished.")

# INSERT DATA INTO THE DATABASE

print("Persisting tweets to the database...")

for tweet in dataStream:
  insertCollection.insert(tweet)

print("OK.")
