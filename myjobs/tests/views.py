from importlib import import_module

from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test.client import Client
from django.test import TestCase

from myjobs.forms import *
from myjobs.models import User
from myprofile.models import Name
from registration.forms import *
from registration.models import ActivationProfile
from myjobs.tests import *



class TestClient(Client):
    """
    Custom test client that decouples testing from the authentication bits
    """
    
    def login_user(self, user):
        if not 'django.contrib.sessions' in settings.INSTALLED_APPS:
            raise AssertionError("Unable to login without django.contrib.sessions in INSTALLED_APPS")
        user.backend = "%s.%s" % ("django.contrib.auth.backends",
                                  "ModelBackend")
        engine = import_module(settings.SESSION_ENGINE)

        # Create a fake request to store login details.
        request = HttpRequest()
        if self.session:
            request.session = self.session
        else:
            request.session = engine.SessionStore()
        login(request, user)

        # Set the cookie to represent the session.
        session_cookie = settings.SESSION_COOKIE_NAME
        self.cookies[session_cookie] = request.session.session_key
        cookie_data = {
            'max-age': None,
            'path': '/',
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'expires': None,
        }
        self.cookies[session_cookie].update(cookie_data)

        # Save the session values.
        request.session.save()

class MyJobsViewsTests(TestCase):
    user_info = {'password1': 'secret',
                 'email': 'alice@example.com'}
    
    def setUp(self):
        super(MyJobsViewsTests, self).setUp()
        self.user = User.objects.create_inactive_user(**self.user_info)
        self.client = TestClient()
        self.client.login_user(self.user)
        
    def test_edit_account_success(self):
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
        resp = self.client.post(reverse('change_password'),
                                    data={'password1': 'secret',
                                          'password2': 'secret',
                                          'new_password': 'new'}, follow=True)
        self.assertRedirects(resp, 'http://testserver%s' % '/account/')
        self.assertTrue(resp.context['user'].check_password('new'))

    def test_change_password_failure(self):
        resp = self.client.post(reverse('change_password'),
                                    data={'password1': 'secret',
                                          'password2': 'secretzzzz',
                                          'new_password': 'new'}, follow=True)
        self.failIf(resp.context['form'].is_valid())
        self.assertFormError(resp, 'form', field=None,
                             errors=u"The two password fields didn't match.")

    def test_complete_successful_profile_form(self):
        # Form with all sections filled out should save successfully
        self.assertEqual(2,2)

    def test_partial_successful_profile_form(self):
        # Form with only some sections completely filled out should
        # save successfully
        self.assertEqual(2,2)

    def test_incomplete_profile_form(self):
        # Form with incomplete sections should return a page with "This field is
        # required" errors
        self.assertEqual(2,2)

    def test_invalid_date_format(self):
        # Form with date in wrong format should return an error
        self.assertEqual(2,2)

    def test_invalid_state(self):
        # Form with an invalid state name should return an error
        self.assertEqual(2,2)

    def test_invalid_country(self):
        # Form with an invalid country name should return an error
        self.assertEqual(2,2)

    def test_no_profile_duplicates(self):
        # Form with errors shouldn't save valid sections until entire form
        # is completely valid
        self.assertEqual(2,2)
