import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse

def validate_search_url(search_url):
    if search_url.find('://') == -1:
        search_url = "http://" + search_url
        
    netloc = 'http://' + urlparse(search_url).netloc
    html = urllib2.urlopen(search_url).read()
    html_soup = BeautifulSoup(html)

    try:
        rss_url = html_soup.find("link",rel="alternate",type="application/rss+xml").attrs['href']
        # relative path needs to be appended to network location
        if rss_url.startswith('/'):
            rss_url = netloc + rss_url
        rss_feed = urllib2.urlopen(rss_url).read()
    
        rss_soup = BeautifulSoup(rss_feed)
    except:
        return None
        
    if rss_soup.find("item"):
        return rss_url
    else:
        return None

def get_feed_title(feed_url):
    feed = urllib2.urlopen(feed_url).read()
    soup = BeautifulSoup(feed)
    return soup.find("title").get_text()
