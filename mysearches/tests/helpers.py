import datetime
from urlparse import urlparse, parse_qs

from django.test import TestCase
from django.core import mail

from testfixtures import Replacer

from mysearches.models import SavedSearch, SavedSearchDigest
from mysearches.helpers import *
from mysearches.tests.test_helpers import return_file
from myjobs.tests.factories import UserFactory

class SavedSearchHelperTests(TestCase):
    def setUp(self):
        super(SavedSearchHelperTests, self).setUp()
        self.user = UserFactory()
        self.valid_url = 'http://www.my.jobs/search?location=chicago&q=nurse'
        
        self.r = Replacer()
        self.r.replace('urllib2.urlopen', return_file)

    def tearDown(self):
        self.r.restore()
        
    def test_valid_dotjobs_url(self):
        url, soup = validate_dotjobs_url(self.valid_url)
        self.assertIsNotNone(url)
        self.assertIsNotNone(soup)

        no_netloc = 'www.my.jobs/search?location=chicago&q=nurse'
        title, url = validate_dotjobs_url(no_netloc)
        self.assertIsNotNone(title)
        self.assertIsNotNone(url)
        self.assertEquals(title, 'Jobs - nurse Jobs in Chicago')

        valid_filter_url = 'www.my.jobs/chicago/illinois/usa/jobs/mcdonalds/careers/'
        title, url = validate_dotjobs_url(valid_filter_url)
        self.assertIsNotNone(title)
        self.assertIsNotNone(url)

    def test_invalid_dotjobs_url(self):
        urls = [ 'http://google.com', # url does not contain a feed
                 '', # url not provided
                 'http://'] # invalid url provided
        for url in urls:
            title, url = validate_dotjobs_url(url)
            self.assertIsNone(title)
            self.assertIsNone(url)

    def test_date_in_range(self):
        start = datetime.date(month=1,day=1,year=2013)
        end = datetime.date(month=12,day=1,year=2013)
        x = datetime.date(month=6,day=1,year=2013)
        is_in_range = date_in_range(start, end, x)
        self.assertTrue(is_in_range)

        start = datetime.date(month=1,day=1,year=2013)
        end = datetime.date(month=12,day=1,year=2013)
        x = datetime.date(month=6,day=1,year=2010)
        is_in_range = date_in_range(start, end, x)
        self.assertFalse(is_in_range)
        
    def test_parse_rss(self):
        feed_url = 'http://www.my.jobs/feed/rss'
        items = parse_rss(feed_url)
        self.assertTrue(len(items) <= 20)

    def test_url_sort_options(self):
        feed = 'http://www.my.jobs/jobs/feed/rss?date_sort=False'

        # Test to make sure sort by "Relevance" has '&date_sort=False' added
        # a single time
        feed_url = url_sort_options(feed, "Relevance")
        parsed = urlparse(feed_url)
        query = parse_qs(parsed.query)

        self.assertEquals(parsed.path, "/jobs/feed/rss")
        self.assertEquals(query['date_sort'], [u'False'])
        int(query['days_ago'][0])
    
        # Test to make sure sort by "Date" doesn't have anything added
        feed_url = url_sort_options(feed, "Date")
        self.assertEquals(feed_url, "http://www.my.jobs/jobs/feed/rss")

    def test_unicode_in_search(self):
        search = SavedSearch(url=u"http://www.my.jobs/search?q=%E2%80%93",
                             user=self.user,
                             feed=u"http://www.my.jobs/search/feed/rss?q=%E2%80%93",
                             sort_by=u'Relevance')
        search.save()

        feed_url = url_sort_options(search.feed, search.sort_by)

        old = parse_qs(urlparse(search.feed).query)
        new = parse_qs(urlparse(feed_url).query)

        self.assertFalse(old.get('date_sort'))
        self.assertFalse(old.get('days_ago'))
        self.assertTrue(new['date_sort'][0])
        self.assertTrue(new['days_ago'][0])

        del new['date_sort']
        del new['days_ago']
        self.assertEqual(new, old)
