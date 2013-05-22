import datetime

from django.conf import settings
from django.contrib.auth import login
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from myjobs.models import User
from myjobs.tests.views import TestClient
from myprofile.models import SecondaryEmail
from registration import forms
from registration.models import ActivationProfile


class RegistrationViewTests(TestCase):
    """
    Test the registration views.

    """
 
    def setUp(self):
        """
        These tests use the default backend, since we know it's
        available; that needs to have ``ACCOUNT_ACTIVATION_DAYS`` set.

        """
        super(RegistrationViewTests, self).setUp()
        self.client = TestClient()
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        if self.old_activation is None:
            settings.ACCOUNT_ACTIVATION_DAYS = 7 # pragma: no cover
        self.data={'email': 'alice@example.com',
                   'password1': 'swordfish',
                   'password2': 'swordfish',
                   'action': 'register'}

    def test_valid_activation(self):
        """
        Test that the ``activate`` view properly handles a valid
        activation (in this case, based on the default backend's
        activation window).

        """
        success_redirect = 'http://testserver%s' % reverse('activate_complete')
        
        # First, register an account.
        self.client.post(reverse('home'), data=self.data)
        profile = ActivationProfile.objects.get(user__email='alice@example.com')
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.failUnless(User.objects.get(email='alice@example.com').is_active)

    def test_anonymous_activation(self):
        """
        Test that the ``activate`` view properly handles activation
        when the user to be activated is not currently logged in.
        """
        # First, register an account.
        self.client.post(reverse('home'), data=self.data)
        self.client.post(reverse('auth_logout'))
        profile = ActivationProfile.objects.get(user__email='alice@example.com')
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.data['email'])

    def test_invalid_activation(self):
        """
        Test that the ``activate`` view properly handles an invalid
        activation (in this case, based on the default backend's
        activation window).

        """
        # Register an account and reset its date_joined to be outside
        # the activation window.
        self.client.post(reverse('home'), data=self.data)
        expired_user = User.objects.get(email='alice@example.com')
        expired_user.date_joined = expired_user.date_joined - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired_user.save()

        expired_profile = ActivationProfile.objects.get(user=expired_user)
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': expired_profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['activated'],
                         expired_profile.activation_key_expired())
        self.failIf(User.objects.get(email='alice@example.com').is_active)
        
    def test_resend_activation(self):
        x, created =User.objects.create_inactive_user(**{'email':'alice@example.com',
                                                         'password1':'secret'})
        self.client.login_user(x)
        self.assertEqual(len(mail.outbox), 1)
        resp = self.client.get('/accounts/register/resend/')
        self.assertEqual(resp.status_code, 200)
        # one email sent for creating an inactive user, another one for resend
        self.assertEqual(len(mail.outbox), 2)

    def test_resend_activation_with_secondary_emails(self):
        user, created = User.objects.create_inactive_user(**{'email':'alice@example.com',
                                                    'password1':'secret'})
        self.assertEqual(ActivationProfile.objects.count(), 1)

        self.client.login_user(user)
        self.client.get('/accounts/register/resend/')
        self.assertEqual(len(mail.outbox), 2)

        SecondaryEmail.objects.create(user=user, email='test@example.com')
        self.assertEqual(ActivationProfile.objects.count(), 2)
        self.client.get('/accounts/register/resend/')
        self.assertEqual(len(mail.outbox), 3)
