import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import pandas as pd
import numpy as np
import json
import time
import os



analyzer = SentimentIntensityAnalyzer()

# establish your credentials; will need to change later using os.environ.get();
#remember to move these credentials to heroku
# Twitter API Keys
consumer_key = os.environ.get('consumer_key')
#config.consumer_key
consumer_secret = os.environ.get('consumer_secret')
#config.consumer_secret
access_token = os.environ.get('access_token')
#config.access_token
access_token_secret = os.environ.get('access_token_secret')
#config.access_token_secret

#set up authentication to Twitter
# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

my_twitter = "@GDBootCamp"

home_twitter_name = "@GDBootCamp"

#create function for analyzing tweets:
def analyze_query_tweet():
# Variables for holding sentiments
    counter = 1
    compound = []

# Loop through 5 pages of tweets (total 100 tweets)
    for x in range(25):

    # Get all tweets from home feed
        public_tweets = api.user_timeline(analysis_target, page=x)

    # Loop through all tweets
        for tweet in public_tweets:

        # Print Tweets
        # print("Tweet %s: %s" % (counter, tweet["text"]))

        # Run Vader Analysis on each tweet
            compound.append(analyzer.polarity_scores(tweet["text"])["compound"])
            tweets_ago = counter

        sentiments_pd = pd.DataFrame({"Compound" : compound})


    plt.plot(np.arange(len(sentiments_pd["Compound"])),
         sentiments_pd["Compound"], marker="o", linewidth=0.5,
         alpha=0.8)

# # Incorporate the other graph properties
    plt.title("Sentiment Analysis of Tweets (%s) for %s" % (time.strftime("%x"), analysis_target))
    plt.legend(title= "Tweets", bbox_to_anchor=(1,1), loc='upper left', labels='@%s' % analysis_target)
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    Chart_file_name = "sentimentAnalysis_" + analysis_target + '.png'
    plt.savefig(Chart_file_name, bbox_inches="tight")
    api.update_with_media(Chart_file_name, "Analysis for a new tweet: @" + analysis_target + ". Thanks" + query_user)
print("Function Works")

#create function for finding tweets:


while(True):

    already_analyzed_users = []
    pub_tweets = api.user_timeline(home_twitter_name, count=100)
    for tweet in pub_tweets:
        try:
            already_analyzed_users.append(tweet['entities']['user_mentions'][0]['screen_name'])
        except:
            continue
    mentions = api.search(q=home_twitter_name, since_id=pub_tweets[0]['id'], result_type='recent')
    for mention in mentions['statuses']:
        if mention["entities"]["user_mentions"][1]["screen_name"] not in already_analyzed_users:
            analysis_target = mention["entities"]["user_mentions"][1]["screen_name"]
            query_user = mention["user"]["screen_name"]
            analyze_query_tweet()
        else:
            print("Already analyzed user.")
            
    time.sleep(300)
