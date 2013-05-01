import simplejson as json

from django.core.urlresolvers import reverse
from django.test import TestCase

from tastypie.models import create_api_key

from myjobs.models import User
from myjobs.tests.factories import UserFactory
from myjobs.tests.views import TestClient
from myprofile.models import SecondaryEmail
from mysearches.models import SavedSearch

class ApiTests(TestCase):
    def setUp(self):
        super(ApiTests, self).setUp()
        self.user = UserFactory()
        self.client = TestClient()
        self.data = {'email':'alice@example.com', 'url':'jobs.jobs/jobs'}
        create_api_key(User, instance=self.user, created=True)

    def test_post_new_search_existing_user(self):
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            format='jsonp',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        search = SavedSearch.objects.all()[0]
        self.assertEqual(search.user, self.user)
        self.assertTrue('testserver' in search.notes)

    def test_post_new_search_new_user(self):
        self.data['email'] = 'new@example.com'
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            format='jsonp',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)
        search = SavedSearch.objects.all()[0]
        user = User.objects.get(email='new@example.com')
        self.assertEqual(search.user, user)

    def test_post_new_search_secondary_email(self):
        SecondaryEmail.objects.create(user=self.user,
                                      email='secondary@example.com')
        self.data['email'] = 'secondary@example.com'
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            format='jsonp',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        search = SavedSearch.objects.all()[0]
        self.assertEqual(search.user, self.user)
        self.assertEqual(search.email, 'secondary@example.com')
