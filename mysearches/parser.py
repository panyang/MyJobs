import feedparser

from urlparser import urlparse

def get_feed_title(feed_url):
    feed_tree = feedparser.parse(feed_url)
    title = feed_tree.feed.title
    return title
