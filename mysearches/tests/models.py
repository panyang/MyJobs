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
        search = SavedSearchFactory(user=self.user, is_active=False,
                                    url='www.my.jobs/search?q=new+search')
        search.send_email()
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox.pop()
        self.assertEqual(email.from_email, settings.SAVED_SEARCH_EMAIL)
        self.assertEqual(email.to, [self.user.email])
        self.assertEqual(email.subject, search.label)
        self.assertTrue("table" in email.body)
        self.assertTrue(email.to[0] in email.body)

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
        self.assertEqual(email.subject, "Your Daily Saved Search Digest")
        self.assertTrue("table" in email.body)
        self.assertTrue(email.to[0] in email.body)

    def test_send_search_digest_send_if_none(self):
        digest = SavedSearchDigestFactory(user=self.user, send_if_none=True)
        digest.send_email()
        self.assertEqual(len(mail.outbox), 0)

        SavedSearchFactory(user=self.user)
        digest.send_email()
        self.assertEqual(len(mail.outbox), 1)
    
    def test_send_initial_email(self):
        search = SavedSearchFactory(user=self.user)
        search = SavedSearchFactory(user=self.user, is_active=False,
                                    url='www.my.jobs/search?q=new+search')
        search.send_initial_email()
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox.pop()
        self.assertEqual(email.from_email, settings.SAVED_SEARCH_EMAIL)
        self.assertEqual(email.to, [self.user.email])
        self.assertEqual("My.jobs New Saved Search" in email.subject, True)
        self.assertTrue("table" in email.body)
        self.assertTrue(email.to[0] in email.body)
    
    def test_send_update_email(self):
        search = SavedSearchFactory(user=self.user)
        search = SavedSearchFactory(user=self.user, is_active=False,
                                    url='www.my.jobs/search?q=new+search')
        search.send_update_email('Your search is updated')
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox.pop()
        self.assertEqual(email.from_email, settings.SAVED_SEARCH_EMAIL)
        self.assertEqual(email.to, [self.user.email])
        self.assertEqual("My.jobs Saved Search Updated" in email.subject, True)
        self.assertTrue("table" in email.body)
        self.assertTrue("Your search is updated" in email.body)
        self.assertTrue(email.to[0] in email.body)