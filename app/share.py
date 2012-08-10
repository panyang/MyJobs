import tweepy
from secrets import *

def gather_access_token(user, provider):
    account = user.social_auth.get(provider=provider)
    access_token = account.extra_data['access_token']
    access_secret = access_token.split('&')[0].split('=')[1]
    access_key = access_token.split('&')[1].split('=')[1]
    return access_key, access_secret
    
def access_twitter_api(user):
    access_key, access_secret = gather_access_token(user, 'twitter')
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)
