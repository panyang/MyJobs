import datetime

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
        self.valid_url = 'http://jobs.jobs/search?location=chicago&q=nurse'
        
        self.r = Replacer()
        self.r.replace('urllib2.urlopen', return_file)

    def tearDown(self):
        self.r.restore()
        
    def test_valid_dotjobs_url(self):
        url, soup = validate_dotjobs_url(self.valid_url)
        self.assertIsNotNone(url)
        self.assertIsNotNone(soup)

        no_netloc = 'jobs.jobs/search?location=chicago&q=nurse'
        title, url = validate_dotjobs_url(no_netloc)
        self.assertIsNotNone(title)
        self.assertIsNotNone(url)
        self.assertEquals(title, 'Jobs - nurse Jobs in Chicago')

        valid_filter_url = 'jobs.jobs/chicago/illinois/usa/jobs/mcdonalds/careers/'
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
        feed_url = 'http://jobs.jobs/feed/rss'
        items = parse_rss(feed_url)
        self.assertTrue(len(items) <= 20)
