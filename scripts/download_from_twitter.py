
# coding: utf-8

# In[2]:

import pandas as pd
import requests
from requests_oauthlib import OAuth1
import cnfg
import tweepy
import csv
import os.path, ConfigParser


# In[3]:
config = ConfigParser.ConfigParser()
config.read("config.ini")
consumer_key =  config.get('twitter', 'consumer_key')
consumer_secret = config.get('twitter', 'consumer_secret')
access_token = config.get('twitter', 'access_token')
access_token_secret = config.get('twitter', 'access_token_secret')


# In[4]:

usernames = set()


# In[5]:

df = pd.read_csv('configuration/CongressTwitterHandles.csv')


# In[6]:

usernames.update(set(df['twitter']))
cleaned = [u for u in list(usernames) if str(u) != 'nan']
usernames=set(cleaned)
len(usernames)


# In[7]:

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
        
    outtweets = [[tweet.id_str, tweet.created_at, screen_name, tweet.retweet_count, tweet.favorite_count, tweet.source.encode("utf-8"), tweet.text.encode("utf-8")] for tweet in alltweets]

    with open('politweets_/%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","user", "retweets", "favorite_count", "source", "text"])
        writer.writerows(outtweets)


# In[16]:

for u in usernames:
    if os.path.isfile('politweets_/%s_tweets.csv' % u):
        print "already collected tweets for %s!" %u
    else:
        try:
            print "getting tweets for %s..." %u
            get_all_tweets(u)
        except:
            print "%s tweets are protected or the API has timed out" %u
    print



