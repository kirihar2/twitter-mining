from dadjokegen.generate import train
from dadjokegen.credentials import Credentials
import tweepy
import os
from datetime import datetime

cred = Credentials()
filename = 'weights/textgenrnn_weights'
auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
auth.set_access_token(cred.access_token, cred.access_secret)
today = datetime.now().strftime("%Y-%m-%d")
filename = os.getcwd()+filename+'-'+today+'.txt'
api = tweepy.API(auth)
print(api.user_timeline('@dadsaysjokes',count=100))


