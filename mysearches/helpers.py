import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
from dateutil import parser as dateparser
import datetime

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
        rss_soup = get_rss_soup(rss_url+'&num_items=1')
    except:
        return None, None

    if rss_soup.find("item"):
        return rss_url, rss_soup
    else:
        return None, None

def get_feed_title(rss_soup):
    return rss_soup.find("title").get_text()

def get_rss_soup(rss_url):
    rss_feed = urllib2.urlopen(rss_url).read()
    return BeautifulSoup(rss_feed)

def parse_rss(feed_url, frequency='W', num_items=20, offset=0):
    rss_soup = get_rss_soup(feed_url+'?num_items='+str(num_items)+'&offset='+str(offset))
    item_list = []
    items = rss_soup.find_all("item")

    if frequency == 'M':
        interval = -30
    elif frequency == 'W':
        interval = -7
    else:
        interval = -1

    end = datetime.date.today()
    start = end + datetime.timedelta(interval)
    
    for item in items:
        item_dict = {}
        item_dict['title'] = item.findChild('title').text
        item_dict['link'] = item.findChild('link').text
        item_dict['pubdate'] = dateparser.parse(item.findChild('pubdate').text)
        item_dict['description'] = item.findChild('description').text

        if date_in_range(start,end,item_dict['pubdate'].date()):
            item_list.append(item_dict)
        else:
            break

    return item_list

def date_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
