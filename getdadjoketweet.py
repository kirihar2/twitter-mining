import tweepy 
from credentials import Credentials
import os
from datetime import datetime
from training_data_pre_processing import TrainingData
def getData():
    cred = Credentials()
    preprocessor = TrainingData()

    auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
    auth.set_access_token(cred.access_token, cred.access_secret)
    today = datetime.now().strftime("%Y-%m-%d")
    filename = 'data/dadjokes-'+today+'.txt'
    api = tweepy.API(auth)
    public_tweets = api.user_timeline('@dadsaysjokes',count=500)
    with open(filename,'w') as out:
        for tweet in public_tweets:
            sanitized_tweet = tweet.text
            sanitized_tweet = preprocessor.filter_url(tweet.text)
            sanitized_tweet = preprocessor.translate_twitter_user_to_generic(sanitized_tweet)
            sanitized_tweet = preprocessor.trim_excess_trailing_chars(sanitized_tweet)
            sanitized_tweet = sanitized_tweet.replace('\n','')
            print(str(sanitized_tweet))
            out.write(str(sanitized_tweet)+'\n')


