import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
from dateutil import parser as dateparser
from datetime import datetime

def validate_search_url(search_url):
    if search_url.find('://') == -1:
        search_url = "http://" + search_url
        
    netloc = 'http://' + urlparse(search_url).netloc
    try:
        html = urllib2.urlopen(search_url).read()
        html_soup = BeautifulSoup(html)
    except:
        return None

    try:
        rss_url = html_soup.find("link",rel="alternate",type="application/rss+xml").attrs['href']
        # relative path needs to be appended to network location
        if rss_url.startswith('/'):
            rss_url = netloc + rss_url
        rss_soup = get_rss_soup(rss_url)
    except:
        return None
        
    if rss_soup.find("item"):
        return rss_url
    else:
        return None

def validate_dotjobs_url(search_url):
    if search_url.find('://') == -1:
        search_url = "http://" + search_url
    parsed = urlparse(search_url)

    rss_url = 'http://' + parsed.netloc + parsed.path + 'feed/rss?' + parsed.query
    
    try:
        rss_soup = get_rss_soup(rss_url)
    except:
        return None

    if rss_soup.find("item"):
        return rss_url
    else:
        return None

def get_feed_title(rss_soup):
    return rss_soup.find("title").get_text()

def get_rss_soup(rss_url):
    rss_feed = urllib2.urlopen(rss_url).read()
    return BeautifulSoup(rss_feed)

def parse_rss_chunk(rss_soup, start=0):
    items = rss_soup.find_all("item")[start:start+20]
    item_list = []
    for item in items:
        item_dict = {}
        item_dict['title'] = item.findChild('title').text
        item_dict['link'] = item.findChild('link').text
        item_dict['pubdate'] = dateparser.parse(item.findChild('pubdate').text)
        item_dict['description'] = item.findChild('description').text
        if datetime.today().date() == item_dict['pubdate'].date():
            item_list.append(item_dict)
    return item_list
