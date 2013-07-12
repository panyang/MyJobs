import base64
import datetime
import pickle
import time

from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.encoding import force_unicode

from myjobs.tests.factories import UserFactory
from myjobs.tests.views import TestClient


class MyJobsHelpersTests(TestCase):
    def setUp(self):
        super(MyJobsHelpersTests, self).setUp()
        self.user = UserFactory()
        self.client = TestClient()

        self.login_params = {'username': 'alice@example.com',
                             'password': 'secret',
                             'action': 'login'}

    def test_login_dont_remember_me(self):
        self.assertEqual(Session.objects.count(), 0)
        response = self.client.post(reverse('home'),
                                    data=self.login_params)
        self.assertEqual(Session.objects.count(), 1)

        session = Session.objects.all()[0]

        session_dict = session.get_decoded()
        user_id = session_dict['_auth_user_id']
        self.assertEqual(user_id, self.user.id)

        # Time zones without using pytz. Fun.
        now = datetime.datetime.now(session.expire_date.tzinfo)
        diff = session.expire_date - now
        self.assertLessEqual(diff.total_seconds(), 900)

    def test_login_remember_me(self):
        self.assertEqual(Session.objects.count(), 0)
        self.login_params['remember_me'] = True
        response = self.client.post(reverse('home'),
                                    data=self.login_params)
        self.assertEqual(Session.objects.count(), 1)

        session = Session.objects.all()[0]

        session_dict = session.get_decoded()
        user_id = session_dict['_auth_user_id']
        self.assertEqual(user_id, self.user.id)

        week = (datetime.datetime.now() + datetime.timedelta(days=14)).toordinal()
        # Session expiration should be two weeks from now - comparing number
        # of days should be good enough
        self.assertEqual(session.expire_date.toordinal(), week)
