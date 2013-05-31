from django.utils import simplejson as json

from django.core.urlresolvers import reverse
from django.test import TestCase

from tastypie.models import create_api_key
from testfixtures import Replacer

from myjobs.models import User
from myjobs.tests.factories import UserFactory
from myjobs.tests.views import TestClient
from myprofile.models import SecondaryEmail
from mysearches.models import SavedSearch
from mysearches.tests.test_helpers import return_file

class UserResourceTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = TestClient()
        self.data = {'email':'foo@example.com'}
        create_api_key(User, instance=self.user, created=True)

    def test_create_new_user(self):
        response = self.client.post(
            '/api/v1/user/',
            data=json.dumps(self.data),
            content_type='application/json',
            HTTP_ACCEPT='text/javascript',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key))
        content = json.loads(response.content)
        self.assertEqual(content, 
            {'user_created':True, 'email':'foo@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(email=self.data['email'])

    def test_no_email(self):
        response = self.client.post(
            '/api/v1/user/',
            data='{}',
            content_type='application/json',
            HTTP_ACCEPT='text/javascript',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['email'], 'No email provided')

    def test_existing_user(self):
        for email in [self.user.email, self.user.email.upper()]:
            self.data['email'] = email
            response = self.client.post(
                '/api/v1/user/',
                data=json.dumps(self.data),
                content_type='application/json',
                HTTP_ACCEPT='text/javascript',
                HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                    (self.user.email, self.user.api_key.key))
            content = json.loads(response.content)
            self.assertEqual(response.status_code, 201)
            self.assertFalse(content['user_created'])
            self.assertEqual(content['email'].lower(), 'alice@example.com')

class SavedSearchResourceTests(TestCase):
    def setUp(self):
        super(SavedSearchResourceTests, self).setUp()
        self.user = UserFactory()
        self.client = TestClient()
        self.data = {'email':'alice@example.com', 'url':'jobs.jobs/jobs'}
        create_api_key(User, instance=self.user, created=True)

        self.r = Replacer()
        self.r.replace('urllib2.urlopen', return_file)

    def tearDown(self):
        self.r.restore()

    def make_response(self, data, *credentials):
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_ACCEPT='text/javascript',
            HTTP_AUTHORIZATION='ApiKey %s' % \
                ':'.join(credentials))
        return response

    def test_new_search_existing_user(self):
        for data in [('alice@example.com', 'jobs.jobs/search?q=django'),
                     ('ALICE@EXAMPLE.COM', 'jobs.jobs/search?q=python')]:
            self.data['email'] = data[0]
            self.data['url'] = data[1]
            response = self.make_response(self.data,
                                          self.user.email,
                                          self.user.api_key.key)
            self.assertEqual(response.status_code, 201)
            search = SavedSearch.objects.all()[0]
            self.assertEqual(search.user, self.user)
            content = json.loads(response.content)
            self.assertEqual(len(content), 3)
            self.assertTrue(content['new_search'])
        self.assertEqual(SavedSearch.objects.filter(user=self.user).count(), 2)

        self.data['url'] = 'http://jobs.jobs/jobs'
        response = self.make_response(self.data,
                                      self.user.email,
                                      self.user.api_key.key)

        for search in SavedSearch.objects.all():
            self.assertTrue('jobs.jobs' in search.notes)

    def test_new_search_new_user(self):
        self.data['email'] = 'new@example.com'
        response = self.make_response(self.data,
                                      self.user.email,
                                      self.user.api_key.key)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SavedSearch.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)
        content = json.loads(response.content)
        self.assertEqual(content['email'], 'No user with email %s exists' % \
                                   self.data['email'])
        self.assertEqual(len(content), 1)

    def test_new_search_secondary_email(self):
        SecondaryEmail.objects.create(user=self.user,
                                      email='secondary@example.com')
        self.data['email'] = 'secondary@example.com'
        response = self.make_response(self.data,
                                      self.user.email,
                                      self.user.api_key.key)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        search = SavedSearch.objects.all()[0]
        self.assertEqual(search.user, self.user)
        self.assertEqual(search.email, 'secondary@example.com')
        content = json.loads(response.content)
        self.assertEqual(len(content), 3)

    def test_new_search_invalid_url(self):
        self.data['url'] = 'google.com'
        response = self.make_response(self.data,
                                      self.user.email,
                                      self.user.api_key.key)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content['url'], 'This is not a valid .JOBS feed')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_new_search_no_url(self):
        del self.data['url']
        response = self.make_response(self.data,
                                      self.user.email,
                                      self.user.api_key.key)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content['url'], 'No .JOBS feed provided')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_no_email(self):
        del self.data['email']
        response = self.make_response(self.data,
                                      self.user.email,
                                      self.user.api_key.key)
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content['email'], 'No email provided')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_no_auth(self):
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, '')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_invalid_auth(self):
        headers = [(self.user.email, 'invalid_key'),
                   ('invalid_user@example.com', self.user.api_key.key),
                   ('invalid_user@example.com', 'invalid_key')]

        for header in headers:
            response = self.make_response(self.data,
                                          *header)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.content, '')
            self.assertEqual(SavedSearch.objects.count(), 0)

    def test_existing_search(self):
        self.make_response(self.data,
                           self.user.email,
                           self.user.api_key.key)
        for email in [self.user.email, self.user.email.upper()]:
            response = self.make_response(self.data,
                                          self.user.email,
                                          self.user.api_key.key)
            content = json.loads(response.content)
            self.assertEqual(len(content), 3)
            self.assertFalse(content['new_search'])
        self.assertEqual(SavedSearch.objects.count(), 1)

    def test_no_day_of(self):
        for frequency in ['W','M']:
            self.data['frequency'] = frequency
            response = self.make_response(self.data,
                                          self.user.email,
                                          self.user.api_key.key)
            content = json.loads(response.content)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(content), 1)
            if frequency == 'W':
                day = 'week'
            else:
                day = 'month'
            self.assertEqual(content['day_of_'+day],
                             'Must supply day_of_'+day)
