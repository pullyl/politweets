#This script downloads historical tweets from representatives
#Requirements - congress-legislators github repo, cloned to the same root of politweets, config.ini with twitter
# consumer keys and access tokens


import pandas as pd
import tweepy
import csv
import os.path, ConfigParser, sys, yaml

output_path = '../raw_data'
input_paths = ['../../congress-legislators/legislators-social-media.yaml',
               '../../congress-legislators/legislators-historical-social-media.yaml']

twitter = 'twitter'
social = 'social'

def main():

    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    consumer_key =  config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')
    access_token = config.get('twitter', 'access_token')
    access_token_secret = config.get('twitter', 'access_token_secret')

    for path in input_paths:
        with open(path, 'r') as stream:
            data_loaded = yaml.load(stream)

        print('loaded %d records from %s' % (len(data_loaded), path))

        usernames = []
        for data in data_loaded:
            if twitter in data[social].keys():
                usernames.append(data[social][twitter])

    summary = []
    for u in usernames:
        file_name = '%s/%s_tweets.csv' % (output_path, u)
        if os.path.isfile(file_name):
            print "already collected tweets for %s at %s" % (u, file_name)
        else:
            try:
                print "getting tweets for %s..." %u
                numtweets = get_all_tweets(u, consumer_key, consumer_secret, access_token, access_token_secret)
                summary.append([u, numtweets])
            except:
                print "%s tweets are protected or the API has timed out" %u
                summary.append([u, sys.exc_info()[0]])
        print_table(summary)
        print

def print_table(table):
    print '----------------------------------------'
    for item in table:
        print '|     ', item[0], ' | ', item[1], '|'
    print '----------------------------------------',

def get_all_tweets(screen_name, consumer_key, consumer_secret, access_token, access_token_secret):
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
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
        
    outtweets = [[tweet.id_str, tweet.created_at, screen_name, tweet.retweet_count, tweet.favorite_count, tweet.source.encode("utf-8"), tweet.text.encode("utf-8")] for tweet in alltweets]

    with open('%s/%s_tweets.csv' % (output_path, screen_name), 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","user", "retweets", "favorite_count", "source", "text"])
        writer.writerows(outtweets)

    print 'collected %d tweets from %s' % (len(outtweets), screen_name)
    return len(outtweets)


main()

