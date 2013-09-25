import datetime

from django.test import TestCase

from myjobs.tests.factories import UserFactory
from mymessages.tests.factories import MessageFactory
from mymessages.models import Message


class MessageTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.message = MessageFactory(user=self.user)

    def test_message_made(self):
        m = Message.objects.filter(user=self.user).count()
        self.assertEqual(m, 1)

    def test_message_unread_default(self):
        m = Message.objects.get(user=self.user)
        self.assertEqual(m.is_unread(), True)

    def test_message_read(self):
        m = Message.objects.get(user=self.user)
        m.mark_read()
        self.assertTrue(m.read_at)

    def test_message_expired(self):
        m = Message.objects.get(user=self.user)
        m.mark_expired()
        self.assertFalse(m.read)
        self.assertTrue(m.expired)
        self.assertTrue(m.expire_at)

    def test_message_expired_w_method(self):
        m = Message.objects.get(user=self.user)
        m.expire_at = datetime.datetime.now() - datetime.timedelta(days=10)
        m.save()
        m.expired_time()
        self.assertTrue(m.expired)

    def test_message_not_expired_w_method(self):
        m = Message.objects.get(user=self.user)
        m.expire_at = datetime.datetime.now() + datetime.timedelta(days=10)
        m.save()
        m.expired_time()
        self.assertFalse(m.expired)