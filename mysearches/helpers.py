import json
import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
from dateutil import parser as dateparser
import datetime

from django.utils import simplejson

from myprofile.models import SecondaryEmail

def validate_dotjobs_url(search_url):
    """
    Validate (but not parse) a .jobs URL. Nothing is returned if the URL has no
    .jobs TLD. 

    Inputs:
    :search_url:   URL to be validated

    Outputs:
    :rss_url:      The corresponding RSS URL. None is returned if not a .jobs URL
    :rss_soup:     The soup object that contains 1 item. Soup is returned if jobs
                   found but None is returned if either the search url is invalid
                   or there were no jobs in the soup.
    """
    if search_url.find('.jobs') == -1:
        return None, None

    if search_url.find('://') == -1:
        search_url = "http://" + search_url
    parsed = urlparse(search_url)

    rss_url = 'http://' + parsed.netloc + parsed.path + 'feed/rss?' + parsed.query
    rss_soup = get_rss_soup(rss_url+'&num_items=1')    
    
    if rss_soup.find("item"):
        return rss_url, rss_soup
    else:
        return rss_url, None

def get_feed_title(rss_soup):
    """
    Finds the title of the RSS feed. 
    
    Inputs:
    :rss_soup:     Soup object of the RSS feed.

    Outputs:
                   String of the RSS feed title.
    """
    
    return rss_soup.find("title").get_text().strip()

def get_rss_soup(rss_url):
    """
    Turn a URL into a BeatifulSoup object
    
    Inputs:
    :rss_url:      URL of an RSS feed

    Outputs:
                   BeautifulSoup object
    """

    rss_feed = urllib2.urlopen(rss_url).read()
    return BeautifulSoup(rss_feed)

def parse_rss(feed_url, frequency='W', num_items=20, offset=0):
    """
    Parses job data from an RSS feed and returns it as a list of dictionaries.
    The data returned is limited based on the corresponding data range (daily,
    weekly, or monthly).
    
    Inputs:
    :feed_url:      URL of an RSS feed
    :frequency:     String 'D', 'W', or 'M'.
    :num_items:     Maximum number of items to be returned.
    :offset:        The page on which the RSS feed is on.

    Outputs:
    :item_list:     List of dictionaries of job data. Each dictionary contains
                    the job title, description, link to the .jobs page, and
                    publish date.
    """

    rss_soup = get_rss_soup(feed_url+'num_items='+str(num_items)+'&offset='+str(offset))
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
            # Since the RSS feeds are ordered by date, we know we can stop once 
            # a job falls out of the date range
            break

    return item_list

def date_in_range(start, end, x):
    """
    Checks if a date object is in a given range of dates.

    Inputs:
    :start:         datetime.date object for the start of the interval
    :end:           datetime.date object for the end of the interval
    :x:             datetime.date object to be checked

    Outputs:
                    Boolean representing if it's in the range
    """

    if start <= end:
        return start <= x <= end
