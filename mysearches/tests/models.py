from django.conf import settings
from django.core import mail
from django.test import TestCase

from testfixtures import Replacer

from myjobs.tests.factories import UserFactory
from mysearches import models
from mysearches.tests.factories import SavedSearchFactory, SavedSearchDigestFactory
from mysearches.tests.test_helpers import fake_render_to_string

class SavedSearchModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

        self.r = Replacer()
        self.r.replace('django.template.loader.render_to_string',
                       fake_render_to_string)

    def tearDown(self):
        self.r.restore()

    def test_send_search_email(self):
        search = SavedSearchFactory(user=self.user)
        search.send_email()
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox.pop()
        self.assertEqual(email.from_email, settings.SAVED_SEARCH_EMAIL)
        self.assertEqual(email.to, [self.user.email])

    def test_send_search_digest_email(self):
        digest = SavedSearchDigestFactory(user=self.user)
        digest.send_email()
        self.assertEqual(len(mail.outbox), 0)

        SavedSearchFactory(user=self.user)
        digest.send_email()
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox.pop()
        self.assertEqual(email.from_email, settings.SAVED_SEARCH_EMAIL)
        self.assertEqual(email.to, [self.user.email])
