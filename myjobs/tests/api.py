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
            content_type='application/json',
            HTTP_ACCEPT='text/javascript',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key))
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        search = SavedSearch.objects.all()[0]
        self.assertEqual(search.user, self.user)
        self.assertTrue('testserver' in search.notes)
        content = json.loads(response.content)
        self.assertEqual(len(content), 4)
        self.assertFalse(content['new_user'])

    def test_post_new_search_new_user(self):
        self.data['email'] = 'new@example.com'
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key)
        )
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)
        search = SavedSearch.objects.all()[0]
        user = User.objects.get(email='new@example.com')
        self.assertEqual(search.user, user)
        content = json.loads(response.content)
        self.assertEqual(len(content), 4)
        self.assertTrue(content['new_user'])

    def test_post_new_search_secondary_email(self):
        SecondaryEmail.objects.create(user=self.user,
                                      email='secondary@example.com')
        self.data['email'] = 'secondary@example.com'
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key))
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        search = SavedSearch.objects.all()[0]
        self.assertEqual(search.user, self.user)
        self.assertEqual(search.email, 'secondary@example.com')
        content = json.loads(response.content)
        self.assertEqual(len(content), 4)
        self.assertFalse(content['new_user'])

    def test_post_new_search_invalid_url(self):
        self.data['url'] = 'google.com'
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key)
        )
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertTrue(content.get('error'))
        self.assertEqual(content['error'], 'This is not a valid .JOBS feed')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_post_new_search_no_url(self):
        del self.data['url']
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key)
        )
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertTrue(content.get('error'))
        self.assertEqual(content['error'], 'This is not a valid .JOBS feed')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_post_no_email(self):
        del self.data['email']
        response = self.client.post(
            '/api/v1/savedsearch/',
            data=json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json',
            HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                (self.user.email, self.user.api_key.key)
        )
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content['error'], 'No email provided')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_post_no_auth(self):
        response = self.client.post(
            '/api/v1/savedsearch/',
            data = json.dumps(self.data),
            HTTP_ACCEPT='text/javascript',
            content_type='application/json'
        )
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, '')
        self.assertEqual(SavedSearch.objects.count(), 0)

    def test_post_invalid_auth(self):
        headers = [(self.user.email, 'invalid_key'),
                   ('invalid_user@example.com', self.user.api_key.key),
                   ('invalid_user@example.com', 'invalid_key')]

        for header in headers:
            response = self.client.post(
                '/api/v1/savedsearch/',
                data = json.dumps(self.data),
                HTTP_ACCEPT='text/javascript',
                content_type='application/json',
                HTTP_AUTHORIZATION='ApiKey %s:%s' % header
            )
            response.content = response.content[9:-1]
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.content, '')
            self.assertEqual(SavedSearch.objects.count(), 0)

    def test_post_existing_search(self):
        def post():
            return self.client.post(
                '/api/v1/savedsearch/',
                data=json.dumps(self.data),
                HTTP_ACCEPT='text/javascript',
                content_type='application/json',
                HTTP_AUTHORIZATION='ApiKey %s:%s' % \
                    (self.user.email, self.user.api_key.key))
        post()
        response = post()
        response.content = response.content[9:-1]
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content['error'], 'User '+self.user.email+\
            ' already has a search for '+self.data['url'])
        self.assertEqual(SavedSearch.objects.count(), 1)
