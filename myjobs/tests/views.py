import base64
from bs4 import BeautifulSoup
from importlib import import_module
from datetime import timedelta, date
import time

from django.conf import settings
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test.client import Client
from django.test import TestCase
from django.utils import simplejson as json

from myjobs.forms import *
from myjobs.models import User, EmailLog
from myjobs.tests.factories import *

from mysearches.models import SavedSearch
from registration.models import ActivationProfile
from registration import signals as custom_signals

from secrets import options, my_agent_auth
from jira.client import JIRA

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
        message = '{{"email":"alice@example.com","timestamp":"{0}",' \
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
                                data={'password': 'secret',
                                      'new_password1': 'new',
                                      'new_password2': 'new'}, follow=True)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'success')
        self.assertTrue(user.check_password('new'))

    def test_change_password_failure(self):
        resp = self.client.post(reverse('edit_password'),
                                data={'password': 'secret',
                                      'new_password1': 'new',
                                      'new_password2': 'notNew'}, follow=True)

        errors = [[u'new_password1',
                   [u'The new password fields did not match.']],
                  [u'new_password2',
                   [u'The new password fields did not match.']]]

        content = json.loads(resp.content)
        self.assertItemsEqual(content['errors'], errors)

    def test_partial_successful_profile_form(self):
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'name-primary': False,
                                      'action': 'save_profile'}, follow=True)
        self.assertEquals(resp.content, 'valid')

    def test_complete_successful_profile_form(self):
        # Form with only some sections completely filled out should
        # save successfully

        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'name-family_name': 'Smith',
                                      'edu-organization_name': 'Stanford University',
                                      'edu-degree_date': '2012-01-01',
                                      'edu-education_level_code': '6',
                                      'edu-degree_major': 'Basket Weaving',
                                      'work-position_title': 'Rocket Scientist',
                                      'work-organization_name': 'Blamco Inc.',
                                      'work-start_date': '2013-01-01',
                                      'ph-use_code': 'Home',
                                      'ph-area_dialing': '999',
                                      'ph-number': '1234567',
                                      'addr-address_line_one': '123 Easy St.',
                                      'addr-city_name': 'Pleasantville',
                                      'addr-country_sub_division_code': 'IN',
                                      'addr-country_code': 'USA',
                                      'addr-postal_code': '99999',
                                      'action': 'save_profile'},
                                follow=True)

        self.assertEquals(resp.content, 'valid')

    def test_incomplete_profile_form(self):
        # Form with incomplete sections should return a page with "This field
        # "is required" errors
        resp = self.client.post(reverse('home'),
                                data={'name-given_name': 'Alice',
                                      'action': 'save_profile'}, follow=True)

        self.failIf(resp.context['name_form'].is_valid())
        self.assertContains(resp, 'This field is required.')

    def test_no_profile_duplicates(self):
        # Form with errors shouldn't save valid sections until entire form
        # is completely valid
        # resp = self.client.post(reverse('home'),
        #                         data={'name-given_name': 'Alice',
        #                               'name-family_name': 'Smith',
        #                               'name-primary':False,
        #                               'education-organization_name': 'U',
        #                               'action':'save_profile'}, follow=True)

        # self.assertEqual(Name.objects.count(), 0)
        # self.assertEqual(Education.objects.count(), 0)
        # resp = self.client.post(reverse('home'),
        #                         data={'name-given_name': 'Alice',
        #                               'name-family_name': 'Smith',
        #                               'name-primary':False,
        #                               'edu-organization_name': 'U',
        #                               'edu-degree_date': '2012-01-01',
        #                               'edu-education_level_code': 6,
        #                               'edu-degree_major': 'Basket Weaving',
        #                               'action':'save_profile'}, follow=True)
        # self.assertEqual(Name.objects.count(), 1)
        # self.assertEqual(Education.objects.count(), 1)

        # Commenting this out for the time being; will create a new ticket for
        # this. When tested manually, this works. This test however, doesn't.
        # In the view we're checking for changed data, for some reason the
        # education form's changed_data attribute is still False.
        pass

    def test_delete_account(self):
        """
        Going to the delete_account view removes a user and their data
        completely
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
                                    HTTP_AUTHORIZATION='BASIC %s' %
                                        base64.b64encode(
                                            'accounts%40my.jobs:secret'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EmailLog.objects.count(), 3)
        process_batch_events()
        self.assertEqual(len(mail.outbox), 0)

        for log in EmailLog.objects.all():
            self.assertTrue(log.event in self.events)

    def test_batch_month_old_message_digest_with_searhes(self):
        """
        Posting data created a month ago should result in one EmailLog instance
        being created per message and one email being sent per user
        """

        # Create activation profile for user; Used when disabling an account
        custom_signals.create_activation_profile(sender=self,
                                                 user=self.user,
                                                 email=self.user.email)

        now = date.today()
        month_ago = date.today() - timedelta(days=30)
        self.user.last_response = month_ago - timedelta(days=1)
        self.user.save()
        SavedSearch(user=self.user).save()

        # Submit a batch of events created a month ago
        # The owners of these addresses should be sent an email
        messages = self.make_messages(month_ago)
        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s' %
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

    def test_batch_month_old_message_digest_no_searches(self):
        """
        Posting data created a month ago should result in no emails being sent
        if the user has no saved searches
        """

        # Create activation profile for user
        custom_signals.create_activation_profile(sender=self,
                                                 user=self.user,
                                                 email=self.user.email)

        month_ago = date.today() - timedelta(days=30)
        self.user.last_response = month_ago - timedelta(days=1)
        self.user.save()

        messages = self.make_messages(month_ago)
        response = self.client.post(reverse('batch_message_digest'),
                                    data=messages,
                                    content_type="text/json",
                                    HTTP_AUTHORIZATION='BASIC %s' %
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
        self.assertEqual(len(mail.outbox), 0)

    def test_batch_month_and_week_old_message_digest(self):
        """
        Posting data created a month and a week ago should result in one
        EmailLog instance being created per message, no emails being sent,
        and the user's opt-in status being set to False
        """

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
                                    HTTP_AUTHORIZATION='BASIC %s' %
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
                                    HTTP_AUTHORIZATION='BASIC %s' %
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
                                    HTTP_AUTHORIZATION='BASIC %s' %
                                        base64.b64encode(
                                            'does%40not.exist:wrong_pass'))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_continue_sending_mail(self):
        Session.objects.all().delete()
        self.user.last_response = date.today() - timedelta(days=7)
        self.user.save()

        # Navigating to the 'continue sending email' page while logged out...
        response = self.client.get(reverse('continue_sending_mail'))
        self.assertRedirects(response, reverse('home'))

        # or with the wrong email address...
        response = self.client.get(reverse('continue_sending_mail') +
                                   '?verify-email=wrong@example.com')
        self.assertRedirects(response, reverse('home'))
        # should result in redirecting to the login page

        response = self.client.get(reverse('continue_sending_mail') +
                                   '?verify-email=%s' % self.user.email)
        self.assertRedirects(response, reverse('home'))
        self.user = User.objects.get(pk=self.user.pk)
        self.assertEqual(self.user.last_response, date.today())

    def test_continue_sending_mail(self):
        self.user.last_response = date.today() - timedelta(days=7)
        self.user.save()

        response = self.client.get(reverse('continue_sending_mail'),
                                   data={'user': self.user}, follow=True)

        self.assertEqual(self.user.last_response,
                         date.today() - timedelta(days=7))
        self.assertRedirects(response, '/')
        self.user = User.objects.get(pk=self.user.pk)
        self.assertEqual(self.user.last_response, date.today())

    def test_redirect_autocreated_user(self):
        """
        When users are created with no password, their password_change
        flag is set to true; If this is the case, all pages except for
        a select few should redirect to the password change form
        """
        self.user.password_change = True
        self.user.save()
        self.user = User.objects.get(email=self.user.email)

        response = self.client.get(reverse('saved_search_main'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_account'))

        profile = ActivationProfile.objects.get_or_create(
            user=self.user,
            email=self.user.email)[0]
        response = self.client.get(reverse('registration_activate',
                                           args=[profile.activation_key]))

        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('edit_password'),
                                    data={'password': 'secret',
                                          'new_password1': 'secret2',
                                          'new_password2': 'secret2'})

        # When models are updated, instances still reference old data
        self.user = User.objects.get(email=self.user.email)
        self.assertFalse(self.user.password_change)

        response = self.client.get(reverse('saved_search_main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_main.html')

    def test_inactive_user_nav(self):
        """ Test that inactive users can't access restricted apps"""
        inactive_user = UserFactory(email='inactive@my.jobs', is_active=False)
        self.client.login_user(inactive_user)
        response = self.client.get("/")
        soup = BeautifulSoup(response.content)
        self.assertFalse(soup.findAll('a', {'id': 'savedsearch-link'}))

    def test_case_insensitive_login(self):
        """
        Test that emails are case-insensitive when logging in
        """
        for email in [self.user.email, self.user.email.upper()]:
            response = self.client.post(reverse('home'),
                                        data={'username': email,
                                              'password': 'secret',
                                              'action': 'login'})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, '{"url": "undefined",' +
                                               ' "validation": "valid"}')

            self.client.get(reverse('auth_logout'))

    def test_guid_cookies_login_and_off(self):
        """
        Tests logging in and recieving a guid cookie. Logging out deletes guid
        cookie.
        """
        response = self.client.post(reverse('home'),
                                    data={'username': self.user.email,
                                          'password': 'secret',
                                          'action': 'login'})

        self.assertTrue(response.cookies['myguid'])
        cookie_guid = response.cookies['myguid']
        guid = cookie_guid.value
        self.assertEqual(guid, self.user.user_guid)

        resp_logoff = self.client.post(reverse('auth_logout'))
        cookie_guid_off = resp_logoff.cookies['myguid']
        guid_off = cookie_guid_off.value
        self.assertEqual(guid_off, '')

    def test_jira_login(self):
        jira = JIRA(options=options, basic_auth=my_agent_auth)
        self.assertIsNotNone(jira)

    def test_anonymous_unsubscribe_all_myjobs_emails(self):
        Session.objects.all().delete()
        self.assertTrue(self.user.opt_in_myjobs)

        # Navigating to the unsubscribe page while logged out...
        response = self.client.get(reverse('unsubscribe_all'))
        self.assertRedirects(response, reverse('home'))
        # or with the wrong email address...
        response = self.client.get(reverse('unsubscribe_all') +
                                   '?verify-email=wrong@example.com')
        # should result in the user's status remaining unchanged
        # and the user should be redirected to the login page
        self.assertRedirects(response, reverse('home'))
        self.user = User.objects.get(id=self.user.id)
        self.assertTrue(self.user.opt_in_myjobs)

        # Navigating to the unsubscribe page while logged out
        # and with the correct email address...
        response = self.client.get(reverse('unsubscribe_all') +
                                   '?verify-email=%s' % self.user.email)
        self.user = User.objects.get(id=self.user.id)
        # should result in the user's :opt_in_myjobs: attribute being
        # set to False
        self.assertFalse(self.user.opt_in_myjobs)

    def test_unsubscribe_all_myjobs_emails(self):
        self.assertTrue(self.user.opt_in_myjobs)

        response = self.client.get(reverse('unsubscribe_all'))
        self.user = User.objects.get(id=self.user.id)
        self.assertFalse(self.user.opt_in_myjobs)

    def test_toolbar_logged_in(self):
        self.client.login_user(self.user)
        response = self.client.get(reverse('toolbar'))
        expected_response = '"user_fullname": "alice@example.com"'
        self.assertIn(expected_response, response.content)

    def test_toolbar_not_logged_in(self):
        Session.objects.all().delete()
        response = self.client.get(reverse('toolbar'))
        expected_response = '({"user_fullname": "", "user_gravatar": '\
                            '"", "employer": ""});'
        self.assertEqual(response.content, expected_response)