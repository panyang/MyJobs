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