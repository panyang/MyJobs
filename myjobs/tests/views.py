from importlib import import_module

from django.conf import settings
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test.client import Client
from django.test import TestCase

from myjobs.forms import *
from myjobs.models import User
from myjobs.tests.factories import *

from myprofile.models import *
from registration.forms import *
from registration.models import ActivationProfile


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
    def setUp(self):
        super(MyJobsViewsTests, self).setUp()
        self.user = UserFactory()
        self.client = TestClient()
        self.client.login_user(self.user)
        
    def test_edit_account_success(self):
        resp = self.client.post(reverse('edit_account'),
                                    data={'given_name': 'Alice',
                                          'family_name': 'Smith',
                                          'gravatar': 'alice@example.com',
                                          'opt_in_myjobs': True}, follow=True)
        name = Name.objects.get(user=resp.context['user'],primary=True)
        self.assertRedirects(resp, 'http://testserver%s' % '/account/')
        self.assertEqual(name.given_name, 'Alice')
        self.assertEqual(name.family_name, 'Smith')
        self.assertEqual(resp.context['user'].opt_in_myjobs, True)

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

    def test_partial_successful_profile_form(self):
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'name-primary':False,
                                      'action':'save_profile'}, follow=True)
        self.assertEquals(resp.content, 'valid')
        
    def test_complete_successful_profile_form(self):
        # Form with only some sections completely filled out should
        # save successfully 
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'name-primary':False,
                                      'education-organization_name': 'Stanford University',
                                      'education-degree_date': '2012-01-01',
                                      'education-education_level_code': 6,
                                      'education-degree_major': 'Basket Weaving',
                                      'employmenthistory-position_title': 'Rocket Scientist',
                                      'employmenthistory-organization_name': 'Blamco Inc.',
                                      'employmenthistory-start_date': '2013-01-01',
                                      'telephone-use_code':'Home',
                                      'telephone-country_dialing': 1,
                                      'telephone-area_dialing': 999,
                                      'telephone-number': 9999,
                                      'address-label': 'Home',
                                      'address-address_line_one': '123 Easy St.',
                                      'address-city_name': 'Pleasantville',
                                      'address-country_sub_division_code': 'IN',
                                      'address-country_code': 'USA',
                                      'address-postal_code': 99999,
                                      'action':'save_profile'}, follow=True)
        self.assertEquals(resp.content, 'valid')

    def test_incomplete_profile_form(self):
        # Form with incomplete sections should return a page with "This field is
        # required" errors
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'name-primary':False,
                                      'education-degree_major': 'Basket Weaving',
                                      'action':'save_profile'}, follow=True)
        self.failIf(resp.context['education_form'].is_valid())
        self.assertContains(resp, 'This field is required.')
        
    def test_no_profile_duplicates(self):
        # Form with errors shouldn't save valid sections until entire form
        # is completely valid
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'name-primary':False,
                                      'education-degree_major': 'Basket Weaving',
                                      'action':'save_profile'}, follow=True)
        self.assertEqual(Name.objects.count(), 0)
        self.assertEqual(Education.objects.count(), 0)
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'name-primary':False,
                                      'education-organization_name': 'Stanford University',
                                      'education-degree_date': '2012-01-01',
                                      'education-education_level_code': 6,
                                      'education-degree_major': 'Basket Weaving',
                                      'action':'save_profile'}, follow=True)
        self.assertEqual(Name.objects.count(), 1)
        self.assertEqual(Education.objects.count(), 1)

    def test_about_template(self):
        # About page should return a status code of 200
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
