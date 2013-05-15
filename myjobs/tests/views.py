import base64
from bs4 import BeautifulSoup
from importlib import import_module
from datetime import timedelta, date
import time

from django.conf import settings
from django.contrib.auth import login
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test.client import Client
from django.test import TestCase
from django.utils.http import urlquote

from myjobs.forms import *
from myjobs.models import User, EmailLog
from myjobs.tests.factories import *

from myprofile.models import *
from registration.forms import *
from registration.models import ActivationProfile
from registration import signals as custom_signals

from tasks import process_batch_events

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
        self.events = ['open', 'delivered', 'click']
        
        self.email_user = UserFactory(email='accounts@my.jobs')

    def make_messages(self, when):
        message = '{{"email":"alice@example.com","timestamp":"{0}",'+\
            '"event":"{1}"}}'
        messages = []
        for event in self.events:
            messages.append(message.format(time.mktime(when.timetuple()),
                                           event))
        return '\r\n'.join(messages)

    def test_edit_account_success(self):
        resp = self.client.post(reverse('edit_account'),
                                    data={'given_name': 'Alice',
                                          'family_name': 'Smith',
                                          'gravatar': 'alice@example.com',
                                          'opt_in_myjobs': True}, follow=True)
        name = Name.objects.get(user=self.user)
        self.assertEqual(name.given_name, 'Alice')
        self.assertEqual(name.family_name, 'Smith')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'success')
        
    def test_change_password_success(self):
        resp = self.client.post(reverse('edit_password'),
                                    data={'password1': 'secret',
                                          'password2': 'secret',
                                          'new_password': 'new'}, follow=True)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'success')
        self.assertTrue(user.check_password('new'))

    def test_change_password_failure(self):
        resp = self.client.post(reverse('edit_password'),
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

    def test_delete_account(self):
        """
        Going to the delete_account view removes a user and their date completely
        """
        self.assertEqual(User.objects.count(), 2)
        resp = self.client.get(reverse('delete_account'), follow=True)
        self.assertEqual(User.objects.count(), 1)

    def test_disable_account(self):
        """
        Going to the disabled account view disables the account, meaning that
        (1) a new activation key is created, (2) User is set to not active and
        (3) User is set to disabled.
        """
        
        user = User.objects.get(id=self.user.id)
        custom_signals.create_activation_profile(sender=self, user=user,
                                                 email=user.email)
        profile = ActivationProfile.objects.get(user=user)
        ActivationProfile.objects.activate_user(profile.activation_key)
        profile = ActivationProfile.objects.get(user=user)
        self.assertEqual(profile.activation_key, 'ALREADY ACTIVATED')

        resp = self.client.get(reverse('disable_account'), follow=True)
        user = User.objects.get(id=self.user.id)
        profile = ActivationProfile.objects.get(user=user)
        self.assertNotEqual(profile.activation_key, 'ALREADY ACTIVATED')
        self.assertFalse(user.is_active)
        self.assertTrue(user.is_disabled)

    def test_about_template(self):
        # About page should return a status code of 200
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_batch_recent_message_digest(self):
        """
        Posting data created recently should result in one EmailLog instance
        being created per message and no emails being sent
        """

        self.client = TestClient()
        # Create activation profile for user; Used when disabling an account
        custom_signals.create_activation_profile(sender=self,
                                                 user=self.user,
                                                 email=self.user.email)

        now = date.today()

        # Submit a batch of three events created recently
        messages = self.make_messages(now)
        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s'%
                                        base64.b64encode(
                                            'accounts%40my.jobs:secret'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EmailLog.objects.count(), 3)
        self.assertEqual(len(mail.outbox), 0)

        for log in EmailLog.objects.all():
            self.assertTrue(log.event in self.events)

    def test_batch_one_month_old_message_digest(self):
        """
        Posting data created a month ago should result in one EmailLog instance
        being created per message and one email being sent per user
        """

        self.client = TestClient()
        # Create activation profile for user; Used when disabling an account
        custom_signals.create_activation_profile(sender=self,
                                                 user=self.user,
                                                 email=self.user.email)

        now = date.today()
        month_ago = date.today() - timedelta(days=30)
        self.user.last_response = month_ago - timedelta(days=1)
        self.user.save()

        # Submit a batch of events created a month ago
        # The owners of these addresses should be sent an email
        messages = self.make_messages(month_ago)
        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s'%
                                        base64.b64encode(
                                            'accounts%40my.jobs:secret'))
        self.assertTrue(response.status_code, 200)
        self.assertEqual(EmailLog.objects.count(), 3)
        self.assertEqual(
            EmailLog.objects.filter(
                received=month_ago
            ).count(), 3
        )
        process_batch_events()
        self.assertEqual(len(mail.outbox), 1)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.last_response, month_ago)

    def test_batch_month_and_week_old_message_digest(self):
        """
        Posting data created a month and a week ago should result in one
        EmailLog instance being created per message, no emails being sent,
        and the user's opt-in status being set to False
        """

        self.client = TestClient()
        # Create activation profile for user; Used when disabling an account
        custom_signals.create_activation_profile(sender=self,
                                                 user=self.user,
                                                 email=self.user.email)

        month_and_week_ago = date.today() - timedelta(days=37)
        self.user.last_response = month_and_week_ago - timedelta(days=1)
        self.user.save()

        # Submit a batch of events created a month and a week ago
        # The owners of these addresses should no longer receive email
        messages = self.make_messages(month_and_week_ago)
        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s'%
                                        base64.b64encode(
                                            'accounts%40my.jobs:secret'))
        self.assertTrue(response.status_code, 200)
        self.assertEqual(EmailLog.objects.count(), 3)
        self.assertEqual(
            EmailLog.objects.filter(
                received__lte=(date.today() - timedelta(days=37))
            ).count(), 3
        )
        process_batch_events()
        self.assertEqual(len(mail.outbox), 0)

        user = User.objects.get(pk=self.user.pk)
        self.assertFalse(user.opt_in_myjobs)
        self.assertTrue(user.last_response, month_and_week_ago)

    def test_invalid_batch_post(self):
        response = self.client.post(reverse('batch_message_digest'),
                                    data='this is invalid',
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s'%
                                        base64.b64encode(
                                            'accounts%40my.jobs:secret'))
        self.assertEqual(response.status_code, 400)

    def test_invalid_user(self):
        now = datetime.datetime.now()
        messages = self.make_messages(now)

        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json")
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s'%
                                        base64.b64encode(
                                            'does%40not.exist:wrong_pass'))
        self.assertEqual(response.status_code, 403)

    def test_continue_sending_mail(self):
        self.user.last_response = date.today() - timedelta(days=7)
        self.user.save()

        response = self.client.get(reverse('continue_sending_mail'),
                                    data={'user': self.user}, follow=True)

        self.assertEqual(self.user.last_response,
                         date.today() - timedelta(days=7))
        self.assertRedirects(response, '/')
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.last_response, date.today())

    def test_redirect_autocreated_user(self):
        """
        When users are created with no password, their password_change
        flag is set to true; If this is the case, all pages except for
        a select few should redirect to the password change form
        """
        self.user.password_change = True
        self.user.save()

        response = self.client.get(reverse('saved_search_main'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_password'))

        response = self.client.get(reverse('registration_activate',
                                   args=['activation_code_here']))

        self.assertEqual(response.status_code, 200)

        self.user.password_change = False
        self.user.save()

        response = self.client.get(reverse('saved_search_main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_main.html')
        
    def test_inactive_user_nav(self):
        """ Test that inactive users can't access restricted apps"""
        inactive_user = UserFactory(email='inactive@my.jobs',is_active=False)
        self.client.login_user(inactive_user)
        response = self.client.get("/")
        soup = BeautifulSoup(response.content)
        self.assertFalse(soup.findAll('a',{'id':'savedsearch_link'}))
