from django.conf import settings
from django.core import mail
from django.test import TestCase

from testfixtures import Replacer

from myjobs.tests.factories import UserFactory
from mysearches import models
from mysearches.tests.factories import SavedSearchFactory, SavedSearchDigestFactory

class SavedSearchModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

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
