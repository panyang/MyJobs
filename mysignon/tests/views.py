import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from myjobs.tests.factories import UserFactory
from myjobs.tests.views import TestClient
from mysignon.models import AuthorizedClient
from mysignon.tests.factories import AuthorizedClientFactory


class MySignOn(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.auth_callback_url = 'https://secure.my.jobs/account'
        self.auth_callback = '?auth_callback=%s' % self.auth_callback_url
        self.key_qs = '%s&key=%s'

        self.client = TestClient()
        self.client.login_user(self.user)

    def test_anonymous_auth(self):
        """
        Anonymous users must first login before being redirected.

        This redirection happens automatically if JavaScript is disabled. JSON
        is returned and the redirect takes place via JavaScript otherwise.
        """
        login_data = {'username': self.user.email,
                      'password': 'secret',
                      'auth_callback': self.auth_callback_url,
                      'action': 'login'}

        self.client.logout()
        self.assertEqual(AuthorizedClient.objects.count(), 0)
        self.assertTrue(self.client.session.get('key') is None)

        response = self.client.post(reverse('sso_authorize'),
                                    login_data)

        self.assertEqual(AuthorizedClient.objects.count(), 1)
        self.assertTrue(self.client.session.get('key') is not None)
        self.assertEqual(response.get('Location'),
                         self.auth_callback_url + '?key=%s' %
                         self.client.session.get('key'))

        self.client.logout()
        response = self.client.post(reverse('sso_authorize'),
                                    login_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        content = json.loads(response.content)
        self.assertEqual(content['url'], self.auth_callback_url +
                         '?key=%s' % self.client.session['key'])

    def test_authenticated_auth(self):
        """
        Users who are already logged in can simply click a button to authorize
        a given site and are then redirected to the given callback url.

        If a given user has already authorized a given site and that site
        provides the key that it was given, this redirect is automatic.
        """
        self.assertEqual(AuthorizedClient.objects.count(), 0)
        self.assertTrue(self.client.session.get('key') is None)

        response = self.client.post(reverse('sso_authorize'),
                                    {'auth_callback': self.auth_callback_url,
                                     'action': 'authorize'})

        self.assertEqual(self.user.authorizedclient_set.count(), 1)
        self.assertTrue(self.client.session.get('key') is not None)
        self.assertEqual(response.get('Location'),
                         self.auth_callback_url + '?key=%s' %
                         self.client.session.get('key'))

        good_qs = self.key_qs % (self.auth_callback,
                                 self.client.session.get('key'))
        response = self.client.get(reverse('sso_authorize') + good_qs)
        self.assertEqual(response.get('Location'),
                         self.auth_callback_url + '?key=%s' %
                         self.client.session.get('key'))

    def test_bad_key(self):
        """
        Providing a bad key will always cause the user to have to
        log back into their account.

        Bad keys are defined as providing a key that doesn't match the
        user's current key or providing a key when the user doesn't currently
        have a key defined.
        """
        # no key
        no_key = self.key_qs % (self.auth_callback,
                                AuthorizedClient.create_key(self.user))
        response = self.client.get(reverse('sso_authorize') + no_key)
        self.assertEqual(AuthorizedClient.objects.count(), 0)

        # Ensure that user was logged out
        response = self.client.get(reverse('view_profile'))
        path = response.request.get('PATH_INFO')
        self.assertRedirects(response, reverse('home')+'?next='+path)

        # wrong key
        self.client.login_user(self.user)
        session = self.client.session
        session['key'] = AuthorizedClient.create_key(self.user)
        session.save()

        # key is a hex string; we can invalidate it by taking a substring
        wrong_key = self.key_qs % (self.auth_callback,
                                   AuthorizedClient.create_key(self.user)[:-1])

        AuthorizedClientFactory(user=self.user)

        response = self.client.get(reverse('sso_authorize') + wrong_key)
        # Ensure that user was logged out again
        response = self.client.get(reverse('view_profile'))
        path = response.request.get('PATH_INFO')
        self.assertRedirects(response, reverse('home')+'?next='+path)
