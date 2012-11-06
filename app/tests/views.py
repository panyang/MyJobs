from django.test import TestCase
from django.core.urlresolvers import reverse
from registration.models import ActivationProfile
from registration.forms import *
from app.forms import *
from app.models import User

class AppViewTests(TestCase):
    def test_home_view_success(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_registration_success(self):
        import ipdb
        ipdb.set_trace()
        response = self.client.post('',
                                   data={'email':'alice@example.com',
                                         'password1': 'password123',
                                         'password2': 'password123'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('register_complete'))
        self.assertEqual(ActivationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)


    def test_home_registration_failure(self):
        self.assertTrue(1,1)
        
    def test_home_login_success(self):
        self.assertTrue(1,1)

    def test_home_login_failure(self):
        self.assertTrue(1,1)

    def test_edit_account_success(self):
        self.assertTrue(1,1)

    def test_edit_account_failure(self):
        self.assertTrue(1,1)

    def test_change_password_success(self):
        self.assertTrue(1,1)

    def test_change_password_failure(self):
        self.assertTrue(1,1)
