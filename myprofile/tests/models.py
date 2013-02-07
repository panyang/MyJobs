from django.core import mail
from django.test import TestCase
from django.core.urlresolvers import reverse

from myjobs.models import User
from myjobs.tests.factories import UserFactory
from myjobs.tests import TestClient
from myprofile.models import *
from myprofile.tests.factories import *
from registration.models import ActivationProfile

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
        secondary_email = SecondaryEmail.objects.get(user=self.user,
                                                     email=secondary_email.email)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(secondary_email.verified)

    def test_set_primary(self):
        """
        Calling the set_as_primary method in the SecondaryEmail removes it from
        SecondaryEmail, replaces the current address on the User model, and
        adds the replaced address to the SecondaryEmail table.

        """
        old_primary = self.user.email
        secondary_email = SecondaryEmailFactory(user=self.user)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        ActivationProfile.objects.activate_user(activation.activation_key)
        secondary_email = SecondaryEmail.objects.get(user=self.user,
                                                     email=secondary_email.email)
        secondary_email.set_as_primary()

        with self.assertRaises(SecondaryEmail.DoesNotExist):
            SecondaryEmail.objects.get(email=secondary_email.email)
        old_email = SecondaryEmail.objects.get(email=old_primary)
        self.assertTrue(old_email.verified)
        user = User.objects.get(email=secondary_email.email)

    def test_unverified_primary_email(self):
        """
        Only verified emails can be set as the primary email
        """

        old_primary = self.user.email
        secondary_email = SecondaryEmailFactory(user=self.user)
        primary = secondary_email.set_as_primary()

        with self.assertRaises(SecondaryEmail.DoesNotExist):
            SecondaryEmail.objects.get(email=old_primary)
        self.assertFalse(primary)
        user = User.objects.get(email=old_primary)
        self.assertEqual(user.email,old_primary)

    def test_maintain_verification_state(self):
        """
        For security reasons, the state of verification of the user email should
        be the same as it is when it is transferred into SecondaryEmail
        """
        
        old_primary = self.user.email
        self.user.is_active=False
        self.user.save()
        secondary_email = SecondaryEmailFactory(user=self.user)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        ActivationProfile.objects.activate_user(activation.activation_key)
        secondary_email = SecondaryEmail.objects.get(user=self.user,
                                                     email=secondary_email.email)
        secondary_email.set_as_primary()

        old_email = SecondaryEmail.objects.get(email=old_primary)
        self.assertFalse(old_email.verified)
        user = User.objects.get(email=secondary_email.email)
