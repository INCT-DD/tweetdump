#!/usr/bin/python3

from bson import json_util
import twint
import contextlib
import pymongo
import sys

# MONGODB AUTH DATA

mongoHost = "127.0.0.1"
mongoPort = "27017"

#Parameters
c = twint.Config()
c.Username = "cabodaciolo"
c.User_full = True
c.Output = "followers.json"
searchLog = "log2.txt"

# RUN TWITTER SEARCH

print("Running search...")

with open(searchLog,'a') as f:
    with contextlib.redirect_stdout(f):
        twint.run.Followers(c)

print("Search finished.")

mongoUrl = ''.join(["mongodb://", mongoUser, ":", mongoPasswd, "@", mongoHost, ":", mongoPort])

try:
  mongoConnection = pymongo.MongoClient(mongoUrl)
  insertDatabase = mongoConnection[searchParameters.Search]
  insertCollection = insertDatabase['followers']
except: 
  print("CONNECTION ERROR. PLEASE CHECK YOUR DATABASE URL")
  sys.exit(1)
  
# LOAD THE DATA FILE

print("Loading data file to memory...")

with open(searchParameters.Output, 'r') as dataFile:
    dataStream = [json_util.loads(line) for line in dataFile]

print("Loading finished.")

# INSERT DATA INTO THE DATABASE

print("Persisting followers to the database...")

for tweet in dataStream:
  insertCollection.insert(tweet)

print("OK.")



