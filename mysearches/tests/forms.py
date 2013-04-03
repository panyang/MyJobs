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
        self.email = self.user.email
        self.choices = ((self.email, self.email),)

    def test_successful_form(self):
        form = SavedSearchForm(user=self.user,data=self.data)
        # Email choices are being set in the view until the model gets changed
        # and users have multiple emails; Once that happens, this will not
        # be necessary
        form.fields['email'].choices = self.choices
        form.fields['email'].initial = self.choices[0][0]
        self.assertTrue(form.is_valid())

    def test_invalid_url(self):
        self.data['url'] = 'http://google.com'
        form = SavedSearchForm(user=self.user,data=self.data)
        form.fields['email'].choices = self.choices
        form.fields['email'].initial = self.choices[0][0]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['url'][0], 'This URL is not valid.')

    def test_day_of_week(self):
        self.data['frequency'] = 'W'
        form = SavedSearchForm(user=self.user,data=self.data)
        form.fields['email'].choices = self.choices
        form.fields['email'].initial = self.choices[0][0]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['day_of_week'][0], 'This field is required.')

        self.data['day_of_week'] = '1'
        form = SavedSearchForm(user=self.user,data=self.data)        
        form.fields['email'].choices = self.choices
        form.fields['email'].initial = self.choices[0][0]
        self.assertTrue(form.is_valid())

    def test_day_of_month(self):
        self.data['frequency'] = 'M'
        form = SavedSearchForm(user=self.user,data=self.data)
        form.fields['email'].choices = self.choices
        form.fields['email'].initial = self.choices[0][0]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['day_of_month'][0], 'This field is required.')

        self.data['day_of_month'] = '1'
        form = SavedSearchForm(user=self.user,data=self.data)        
        form.fields['email'].choices = self.choices
        form.fields['email'].initial = self.choices[0][0]
        self.assertTrue(form.is_valid())
        
