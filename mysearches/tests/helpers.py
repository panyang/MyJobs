import datetime

from django.test import TestCase
from django.core import mail

from mysearches.models import SavedSearch, SavedSearchDigest
from mysearches.helpers import *
from myjobs.tests.factories import UserFactory

class SavedSearchHelperTests(TestCase):
    def setUp(self):
        super(SavedSearchHelperTests, self).setUp()
        self.user = UserFactory()
        self.valid_url = 'http://jobs.jobs/search?location=chicago&q=nurse'
        
    def test_valid_dotjobs_url(self):
        url, soup = validate_dotjobs_url(self.valid_url)
        self.assertIsNotNone(url)
        self.assertIsNotNone(soup)

        no_netloc = 'jobs.jobs/search?location=chicago&q=nurse'
        url, soup = validate_dotjobs_url(no_netloc)
        self.assertIsNotNone(url)
        self.assertIsNotNone(soup)

        valid_filter_url = 'jobs.jobs/chicago/illinois/usa/jobs/mcdonalds/careers/'
        url, soup = validate_dotjobs_url(valid_filter_url)
        self.assertIsNotNone(url)
        self.assertIsNotNone(soup)

    def test_invalid_dotjobs_url(self):
        invalid_url = 'http://google.com'
        url, soup = validate_dotjobs_url(invalid_url)
        self.assertIsNone(url)
        self.assertIsNone(soup)

    def test_get_feed_title(self):
        soup = get_rss_soup(self.valid_url)
        title = get_feed_title(soup)
        self.assertEquals(title, 'Jobs - nurse Jobs in Chicago')

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
        
