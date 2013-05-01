import datetime

from django.conf import settings
from django.contrib.auth import login
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from myjobs.models import User
from myjobs.tests.views import TestClient
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

            
    def test_registration_view_initial(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'registration/registration_form.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.RegistrationForm))

    def test_registration_view_success(self):
        response = self.client.post('/accounts/register/',
                                    data={'email': 'bob@example.com',
                                          'password1': 'password123',
                                          'password2': 'password123'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('register_complete'))
        self.assertEqual(ActivationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_valid_activation(self):
        """
        Test that the ``activate`` view properly handles a valid
        activation (in this case, based on the default backend's
        activation window).

        """
        success_redirect = 'http://testserver%s' % reverse('activate_complete')
        
        # First, register an account.
        self.client.post(reverse('register'),
                         data={'email': 'alice@example.com',
                               'password1': 'swordfish',
                               'password2': 'swordfish'})
        profile = ActivationProfile.objects.get(user__email='alice@example.com')
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.failUnless(User.objects.get(email='alice@example.com').is_active)

    def test_invalid_activation(self):
        """
        Test that the ``activate`` view properly handles an invalid
        activation (in this case, based on the default backend's
        activation window).

        """
        # Register an account and reset its date_joined to be outside
        # the activation window.
        self.client.post(reverse('register'),
                         data={'email': 'bob@example.com',
                               'password1': 'secret',
                               'password2': 'secret'})
        expired_user = User.objects.get(email='bob@example.com')
        expired_user.date_joined = expired_user.date_joined - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired_user.save()

        expired_profile = ActivationProfile.objects.get(user=expired_user)
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': expired_profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['activated'],
                         expired_profile.activation_key_expired())
        self.failIf(User.objects.get(email='bob@example.com').is_active)
        
    def test_resend_activation(self):
        x, created =User.objects.create_inactive_user(**{'email':'alice@example.com',
                                                         'password1':'secret'})
        self.client.login_user(x)
        self.assertEqual(len(mail.outbox), 1)
        resp = self.client.get('/accounts/register/resend/')
        self.assertEqual(resp.status_code, 200)
        # one email sent for creating an inactive user, another one for resend
        self.assertEqual(len(mail.outbox), 2)

