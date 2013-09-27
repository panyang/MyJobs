import datetime

from django.test import TestCase
from django.contrib.auth.models import Group

from myjobs.tests.factories import UserFactory
from myjobs.models import User
from mymessages.models import Message, MessageInfo


class MessageTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.message = Message(subject='subject',
                               body='body',
                               message_type='success',
                               active=True)
        self.message.save()
        for group in Group.objects.all():
            self.message.group.add(group.pk)
        self.message.save()
        self.messageInfo = MessageInfo(user=User.objects.get(id=1),
                                       message=self.message)
        self.messageInfo.save()

    def test_message_made(self):
        m = Message.objects.all().count()
        self.assertEqual(m, 1)

    def test_message_made_sent_to_multiple(self):
        m = Message.objects.all().count()
        UserFactory(email="Best@best.com")
        n_u = User.objects.get(email="Best@best.com")
        n_u.groups.add(Group.objects.get(id=1).pk)
        n_u.save()
        n_u.check_messages()
        message_info = MessageInfo.objects.all().count()
        self.assertEqual(m, 1)
        self.assertEqual(message_info, 2)

    def test_message_unread_default(self):
        m = self.messageInfo
        self.assertEqual(m.is_unread(), True)

    def test_message_read(self):
        m = self.messageInfo
        m.mark_read()
        self.assertTrue(m.read_at)

    def test_message_expired(self):
        m = self.messageInfo
        m.mark_expired()
        self.assertFalse(m.read)
        self.assertTrue(m.expired)
        self.assertTrue(m.expired_on)

    def test_message_expired_w_method(self):
        m = self.messageInfo
        m.message.expire_at = datetime.datetime.now() - \
                              datetime.timedelta(days=20)
        m.message.save()
        m.expired_time()
        self.assertTrue(m.expired)

    def test_message_not_expired_w_method(self):
        m = self.messageInfo
        m.message.expire_at = datetime.datetime.now() + \
                              datetime.timedelta(days=10)
        m.message.save()
        m.expired_time()
        self.assertFalse(m.expired)