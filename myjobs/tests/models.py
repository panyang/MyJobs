import urllib
from django.core import mail
from django.test import TestCase

from myjobs.models import *
from myjobs.tests.factories import *


class UserManagerTests(TestCase):
    user_info = {'password1': 'complicated_password',
                 'email': 'alice@example.com'}

    def test_inactive_user_creation(self):
        new_user = User.objects.create_inactive_user(**self.user_info)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_active, False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))


    def test_active_user_creation(self):
        new_user = User.objects.create_user(**self.user_info)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))

    def test_superuser_creation(self):
        new_user = User.objects.create_superuser(**{'password': 'complicated_password',
                                                    'email': 'alice@example.com'})
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_superuser, True)
        self.assertEqual(new_user.is_staff, True)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))

    def test_gravatar_url(self):
        """
        Test that email is hashed correctly and returns a 200 response
        """
        user = UserFactory()
        static_gravatar_url = "http://www.gravatar.com/avatar/c160f8cc69a4f0b" \
                              "f2b0362752353d060?s=20&d=mm"
        generated_gravatar_url = user.get_gravatar_url()
        self.assertEqual(static_gravatar_url, generated_gravatar_url)
        status_code = urllib.urlopen(static_gravatar_url).getcode()
        self.assertEqual(status_code, 200)
