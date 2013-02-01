from django.core import mail
from django.test import TestCase

from myjobs.models import *
from myjobs.tests.factories import UserFactory
from myjobs.tests import TestClient
from myprofile.models import *
from myprofile.tests.factories import *


class MyProfileTests(TestCase):
    user_info = {'password1': 'complicated_password',
                 'email': 'alice@example.com'}

    def setUp(self):
        super(MyProfileTests, self).setUp()
        self.user = UserFactory()

    def test_primary_name_save(self):
        """
        Saving a primary name when one already exists replaces it with
        the new primary name.
        """

        initial_name = PrimaryNameFactory()
        
        self.assertTrue(initial_name.primary)
        new_primary_name = NewPrimaryNameFactory()
        initial_name = Name.objects.get(given_name='Alice')
        self.assertTrue(new_name.primary)
        self.assertFalse(initial_name.primary)

    def test_email_activation_creation(self):
        """
        Creating a new secondary email creates a corresponding unactivated
        ActivationProfile.
        """
        secondary_email = SecondaryEmailFactory()
        activation = ActivationProfile.objects.get(email=secondary_email.email)
        self.assertEqual(secondary_email.email, activation.email)
