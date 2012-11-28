from django.contrib.auth import login
from django.test import TestCase
from django.core.urlresolvers import reverse
from registration.models import ActivationProfile
from registration.forms import *
from myjobs.forms import *
from myjobs.models import User

class AppViewTests(TestCase):
    def test_edit_account_success(self):
        user = User.objects.create_user(**{'email':'alice@example.com',
                                           'password1':'secret'})
        self.client.login(username='alice@example.com',
                          password='secret')
        resp = self.client.post(reverse('edit_account'),
                                    data={'first_name': 'Alice',
                                          'last_name': 'Smith',
                                          'opt_in_myjobs': True}, follow=True)
        self.assertRedirects(resp, 'http://testserver%s' % '/account/')
        self.assertEqual(resp.context['user'].first_name, 'Alice')
        self.assertEqual(resp.context['user'].last_name, 'Smith')
        self.assertEqual(resp.context['user'].opt_in_myjobs, True)\

    def test_change_password_success(self):
        user = User.objects.create_user(**{'email':'alice@example.com',
                                           'password1':'secret'})
        self.client.login(username='alice@example.com',
                          password='secret')
        resp = self.client.post(reverse('change_password'),
                                    data={'password1': 'secret',
                                          'password2': 'secret',
                                          'new_password': 'new'}, follow=True)
        self.assertRedirects(resp, 'http://testserver%s' % '/account/')
        self.assertTrue(resp.context['user'].check_password('new'))

    def test_change_password_failure(self):
        user = User.objects.create_user(**{'email':'alice@example.com',
                                           'password1':'secret'})
        self.client.login(username='alice@example.com',
                          password='secret')
        resp = self.client.post(reverse('change_password'),
                                    data={'password1': 'secret',
                                          'password2': 'secretzzzz',
                                          'new_password': 'new'}, follow=True)
        self.failIf(resp.context['form'].is_valid())
        self.assertFormError(resp, 'form', field=None,
                             errors=u"The two password fields didn't match.")
