from django.core import mail
from django.test import TestCase
from django.core.urlresolvers import reverse

from myjobs.models import User
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

        initial_name = PrimaryNameFactory(user=self.user)
        
        self.assertTrue(initial_name.primary)
        new_name = NewPrimaryNameFactory(user=self.user)
        initial_name = Name.objects.get(given_name='Alice')
        self.assertTrue(new_name.primary)
        self.assertFalse(initial_name.primary)

    def test_email_activation_creation(self):
        """
        Creating a new secondary email creates a corresponding unactivated
        ActivationProfile.
        """
        
        secondary_email = SecondaryEmailFactory(user=self.user)
        activation = ActivationProfile.objects.get(email=secondary_email.email)
        self.assertEqual(secondary_email.email, activation.email)

    def test_send_activation(self):
        """
        The send_activation method in SecondaryEmail should send an
        activation link to the email address
        """

        secondary_email = SecondaryEmailFactory(user=self.user)
        secondary_email.send_activation()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [secondary_email.email])

    def test_verify_email(self):
        """
        Clicking the activation link sets the ActivationProfile object to
        activated and sets the SecondaryEmail object to verified.
        """

        secondary_email = SecondaryEmailFactory(user=self.user)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key':
                                                   activation.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.failUnless(secondary_email.verified)
