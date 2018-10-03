import tweepy
import sys
import pymongo
from bson import json_util

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

mongoUser =""  
mongoPasswd =""
mongoHost = "127.0.0.1"
mongoPort = "27017"

##################################
replies=[]
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  

name= ""
for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(10):

  for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(1000):

    if hasattr(tweet, 'in_reply_to_status_id_str'):
      if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
         replies.append(tweet)
         print("Tweet :",full_tweets.text.translate(non_bmp_map))
         print(tweet.user.screen_name, " reply: ", tweet.text) 


# BUILD MONGO URL AND CONNECT TO DATABASE

mongoUrl = ''.join(["mongodb://", mongoUser, ":", mongoPasswd, "@", mongoHost, ":", mongoPort])

try:
  mongoConnection = pymongo.MongoClient(mongoUrl)
  insertDatabase = mongoConnection["testdb"]
  insertCollection = insertDatabase['replies']
except: 
  print("CONNECTION ERROR. PLEASE CHECK YOUR DATABASE URL")
  sys.exit(1)


# INSERT DATA INTO THE DATABASE

print("Persisting tweets to the database...")

for reply in replies:
  insertCollection.insert(reply) 
