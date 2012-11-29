from django.test import TestCase
from django.core import mail
from myjobs.models import *

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
