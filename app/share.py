import tweepy
import facebook
from secrets import *
from default_settings import *
import oauth2 as oauth
import xml.etree.ElementTree as ET
from xml.etree import *
from xml.dom.minidom import Document

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

def access_linkedin_api(user):
    access_key, access_secret = gather_access_token(user, 'linkedin')
    token = oauth.Token(key=access_key, secret=access_secret)
    consumer = oauth.Consumer(key=LINKEDIN_CONSUMER_KEY,
                              secret=LINKEDIN_CONSUMER_SECRET)
    return  oauth.Client(consumer=consumer, token=token)

def access_facebook_api(user):
    access_token = user.social_auth.get(provider='facebook').extra_data['access_token']
    return facebook.GraphAPI(access_token)

def build_linkedin_share(comment,
                         title=SHARE_DEFAULT_TITLE,
                         description=SHARE_DEFAULT_URL_DESCRIPTION,
                         submitted_url=SHARE_DEFAULT_URL,
                         submitted_image_url="http://src.nlx.org/myjobs/icon-80x80.png",
                         code="anyone"):
    
    base = '<?xml version="1.0" encoding="UTF-8"?>'
    status_tree = ET.Element('share')
    
    st_comment = ET.SubElement(status_tree, 'comment')
    st_comment.text = comment
    
    st_content = ET.SubElement(status_tree, 'content')
    st_title = ET.SubElement(st_content, 'title')
    st_title.text = title
    st_description = ET.SubElement(st_content, 'description')
    st_description.text = description
    st_submitted_url = ET.SubElement(st_content, 'submitted-url')
    st_submitted_url.text = submitted_url
    st_submitted_image_url = ET.SubElement(st_content, 'submitted-image-url')
    st_submitted_image_url.text = submitted_image_url
    
    st_visibility = ET.SubElement(status_tree, 'visibility')
    st_code = ET.SubElement(st_visibility, 'code')
    st_code.text = code
    return base + ET.tostring(status_tree)
