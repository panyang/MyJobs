from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.test import TestCase

from myjobs.forms import *
from myjobs.models import User
from myprofile.models import Name
from registration.forms import *
from registration.models import ActivationProfile

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
        name = Name.objects.get(user=resp.context['user'],primary=True)
        self.assertRedirects(resp, 'http://testserver%s' % '/account/')
        self.assertEqual(name.given_name, 'Alice')
        self.assertEqual(name.family_name, 'Smith')
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
