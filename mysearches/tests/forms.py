from django.test import TestCase

from mysearches.models import SavedSearch, SavedSearchDigest
from mysearches.forms import SavedSearchForm
from myjobs.tests.factories import UserFactory

class SavedSearchFormTests(TestCase):
    def setUp(self):
        super(SavedSearchFormTests, self).setUp()
        self.user = UserFactory()
        self.data = {'url': 'http://jobs.jobs/jobs',
                     'feed': 'http://jobs.jobs/jobs/feed/rss?',
                     'email': 'alice@example.com',
                     'frequency': 'D',
                     'label': 'All jobs from jobs.jobs'}

    def test_successful_form(self):
        form = SavedSearchForm(user=self.user,data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_url(self):
        self.data['url'] = 'http://google.com'
        form = SavedSearchForm(user=self.user,data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['url'][0], 'This URL is not valid.')

    def test_day_of_week(self):
        self.data['frequency'] = 'W'
        form = SavedSearchForm(user=self.user,data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['day_of_week'][0], 'This field is required.')

        self.data['day_of_week'] = '1'
        form = SavedSearchForm(user=self.user,data=self.data)        
        self.assertTrue(form.is_valid())

    def test_day_of_month(self):
        self.data['frequency'] = 'M'
        form = SavedSearchForm(user=self.user,data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['day_of_month'][0], 'This field is required.')

        self.data['day_of_month'] = '1'
        form = SavedSearchForm(user=self.user,data=self.data)        
        self.assertTrue(form.is_valid())
        
