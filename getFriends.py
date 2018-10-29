import tweepy
import sys
import pymongo
import json
import csv
import time
from bson import json_util

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
#Persistence
mongoUser =""  
mongoPasswd =""
mongoHost = ""
mongoPort = "27017"
mongoUrl = ''.join(["mongodb://", mongoUser, ":", mongoPasswd, "@", mongoHost, ":", mongoPort])


try:
    mongoConnection = pymongo.MongoClient(mongoUrl)
    insertDatabase = mongoConnection["testdb"]
    insertCollection = insertDatabase['friends']
except: 
    print("CONNECTION ERROR. PLEASE CHECK YOUR DATABASE URL")
    sys.exit(1)

#INSERT DATA INTO THE DATABASE
def process_or_store(friend):
    #print("Persisting tweets to the database...")
    reply= dict(friend)
    insertCollection.insert_one(friend) 

# CSV
csvFile = open('friends.csv', 'a')

csvWriter = csv.writer(csvFile)


candidate_name= ""
users = tweepy.Cursor(api.friends, screen_name=candidate_name).items()

for user in users:
    print(user.screen_name)
    process_or_store(user._json)
    csvWriter.writerow([candidate_name, user.id_str, user.screen_name])
    

csvFile.close()


