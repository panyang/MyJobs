from django.test import TestCase
from django.core.urlresolvers import reverse

from myjobs.tests.factories import UserFactory
from myjobs.tests.views import TestClient
from mymessages.tests.factories import MessageFactory
from mymessages.models import Message


class MessageViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.message = MessageFactory(user=self.user)
        self.client = TestClient()
        self.client.login_user(self.user)

    def test_user_post_mark_message_read(self):
        resp = self.client.post(reverse('read'),
                                data={'name': 'message-'+str(self.message.id)
                                              + '-'+str(self.user.id)},
                                follow=True)
        m = Message.objects.get(user=self.user)
        self.assertTrue(m.read)
        self.assertTrue(m.read_at)