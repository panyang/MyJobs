from django.core.urlresolvers import reverse
from django.test import TestCase

from myjobs.tests.factories import UserFactory
from myjobs.tests.views import TestClient
from sso.models import AuthorizedClient
from sso.tests.factories import AuthorizedClientFactory


class SSOViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.referer = 'http://my.jobs'
        self.callback_url = self.referer + '/account'
        self.callback = '?callback=%s' % self.callback_url
        self.key_qs = '%s&key=%s'

        self.client = TestClient()
        self.client.login_user(self.user)

    def test_mismatched_referer_callback(self):
        """
        The callback url is expected to be from the same domain as the
        HTTP referer. Anything else will display a 404 page.
        """
        response = self.client.get(reverse('sso_authorize') +
                                   '?callback=http://jobs.jobs',
                                   HTTP_REFERER=self.referer)
        self.assertEqual(response.status_code, 404)

    def test_unbalanced_referer_callback(self):
        """
        A callback url and HTTP referer are required. If one is missing,
        dispaly a 404 page.
        """
        response = self.client.get(reverse('sso_authorize') + self.callback)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('sso_authorize'),
                                   HTTP_REFERER=self.referer)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('sso_authorize') + self.callback,
                                   HTTP_REFERER=self.referer)
        self.assertTemplateUsed(response, 'sso/sso_auth.html')

    def test_anonymous_auth(self):
        """
        Anonymous users must first login before being redirected.

        This redirection happens automatically.
        """
        self.client.logout()
        self.assertEqual(AuthorizedClient.objects.count(), 0)
        self.assertTrue(self.client.session.get('key') is None)

        response = self.client.post(reverse('sso_authorize'),
                                    {'username': self.user.email,
                                     'password': 'secret',
                                     'callback': self.callback_url,
                                     'referer': self.referer,
                                     'action': 'login'})

        self.assertEqual(AuthorizedClient.objects.count(), 1)
        self.assertTrue(self.client.session.get('key') is not None)
        self.assertEqual(response.get('Location'),
                         self.callback_url + '?key=%s' %
                         self.client.session.get('key'))

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
                                    {'callback': self.callback_url,
                                     'referer': self.referer,
                                     'action': 'authorize'})

        self.assertEqual(self.user.authorizedclient_set.count(), 1)
        self.assertTrue(self.client.session.get('key') is not None)
        self.assertEqual(response.get('Location'),
                         self.callback_url + '?key=%s' %
                         self.client.session.get('key'))

        good_qs = self.key_qs % (self.callback, self.client.session.get('key'))
        response = self.client.get(reverse('sso_authorize') + good_qs,
                                   HTTP_REFERER=self.referer)
        self.assertEqual(response.get('Location'),
                         self.callback_url + '?key=%s' %
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
        no_key = self.key_qs % (self.callback,
                                AuthorizedClient.create_key(self.user))
        response = self.client.get(reverse('sso_authorize') + no_key,
                                   HTTP_REFERER=self.referer)
        self.assertEqual(AuthorizedClient.objects.count(), 0)

        # Ensure that user was logged out
        response = self.client.get(reverse('view_profile'))
        self.assertRedirects(response, reverse('home'))

        # wrong key
        self.client.login_user(self.user)
        session = self.client.session
        session['key'] = AuthorizedClient.create_key(self.user)
        session.save()

        # key is a hex string; we can invalidate it by taking a substring
        wrong_key = self.key_qs % (self.callback,
                                   AuthorizedClient.create_key(self.user)[:-1])

        AuthorizedClientFactory(user=self.user)

        response = self.client.get(reverse('sso_authorize') + wrong_key,
                                   HTTP_REFERER=self.referer)
        # Ensure that user was logged out again
        response = self.client.get(reverse('view_profile'))
        self.assertRedirects(response, reverse('home'))
