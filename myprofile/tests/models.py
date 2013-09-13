from django.core import mail
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase

from myjobs.models import User
from myjobs.tests.factories import UserFactory
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

    def test_primary_name_save_multiuser(self):
        """
        Saving primary names when multiple users are present accurately
        sets and retrieves the correct name
        """
        self.user_2 = UserFactory(email='foo@example.com')
        user_2_initial_name = PrimaryNameFactory(user=self.user_2)
        user_2_new_name = NewPrimaryNameFactory(user=self.user_2)

        initial_name = PrimaryNameFactory(user=self.user)
        new_name = NewPrimaryNameFactory(user=self.user)

        user_2_initial_name = Name.objects.get(given_name='Alice',
                                               user=self.user_2)
        user_2_new_name = Name.objects.get(given_name='Alicia',
                                           user=self.user_2)
        initial_name = Name.objects.get(given_name='Alice', user=self.user)

        self.assertTrue(new_name.primary)
        self.assertFalse(initial_name.primary)
        self.assertTrue(user_2_new_name.primary)
        self.assertFalse(user_2_initial_name.primary)

        with self.assertRaises(MultipleObjectsReturned):
            Name.objects.get(primary=True)
            Name.objects.get(primary=False)
            Name.objects.get(given_name='Alice')
            Name.objects.get(given_name='Alicia')
        Name.objects.get(primary=True, user=self.user_2)

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
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [secondary_email.email])
        self.assertTrue('secondary email' in mail.outbox[0].body)

    def test_verify_email(self):
        """
        Clicking the activation link sets the ActivationProfile object to
        activated and sets the SecondaryEmail object to verified.
        """

        secondary_email = SecondaryEmailFactory(user=self.user)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        response = self.client.get(reverse('registration_activate',
                                           args=[activation.activation_key]) +
                                   '?verify-email=%s' % self.user.email)
        secondary_email = SecondaryEmail.objects.get(user=self.user,
                                                     email=secondary_email.email)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(secondary_email.verified)

    def test_set_primary_email(self):
        """
        Calling the set_as_primary method in the SecondaryEmail removes it from
        SecondaryEmail, replaces the current address on the User model, and
        adds the replaced address to the SecondaryEmail table.

        """
        old_primary = self.user.email
        secondary_email = SecondaryEmailFactory(user=self.user)
        new_primary = secondary_email.email

        for email in [old_primary, new_primary]:
            # Emails must be verified to make them primary.
            activation = ActivationProfile.objects.get_or_create(user=self.user,
                                                                 email=email)[0]
            ActivationProfile.objects.activate_user(activation.activation_key)

        secondary_email = SecondaryEmail.objects.get(email=new_primary)
        secondary_email.set_as_primary()

        with self.assertRaises(SecondaryEmail.DoesNotExist):
            SecondaryEmail.objects.get(email=new_primary)
        old_email = SecondaryEmail.objects.get(email=old_primary)
        self.assertTrue(old_email.verified)
        user = User.objects.get(email=new_primary)

    def test_duplicate_same_primary_name(self):
        """
        Makes sure that one can not create duplicate primary names.
        """
        primary_name1 = PrimaryNameFactory(user=self.user)
        primary_name2 = PrimaryNameFactory(user=self.user)

        num_results = self.user.profileunits_set.filter(
            content_type__name='name').count()
        self.assertEqual(num_results, 1)

    def test_different_primary_name(self):
        primary_name1 = PrimaryNameFactory(user=self.user)
        primary_name2 = NewPrimaryNameFactory(user=self.user)

        primary_name_count = Name.objects.filter(user=self.user,
                                                 primary=True).count()
        non_primary_name_count = Name.objects.filter(user=self.user,
                                                     primary=False).count()

        self.assertEqual(primary_name_count, 1)
        self.assertEqual(non_primary_name_count, 1)

    def test_non_primary_name_to_primary(self):
        name = NewNameFactory(user=self.user)
        primary_name1 = PrimaryNameFactory(user=self.user)

        primary_name_count = Name.objects.filter(user=self.user,
                                                 primary=True).count()
        non_primary_name_count = Name.objects.filter(user=self.user,
                                                     primary=False).count()

        self.assertEqual(primary_name_count, 1)
        self.assertEqual(non_primary_name_count, 0)

    def test_primary_name_to_non_primary(self):
        primary_name = PrimaryNameFactory(user=self.user)
        primary_name.primary = False
        primary_name.save()

        primary_name_count = Name.objects.filter(user=self.user,
                                                 primary=True).count()
        non_primary_name_count = Name.objects.filter(user=self.user,
                                                     primary=False).count()

        self.assertEqual(primary_name_count, 0)
        self.assertEqual(non_primary_name_count, 1)

    def test_duplicate_name(self):
        """
        Makes sure that duplicate names is not saving.
        """
        name1 = NewNameFactory(user=self.user)
        name2 = NewNameFactory(user=self.user)

        num_results = Name.objects.filter(user=self.user).count()
        self.assertEqual(num_results, 1)

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
        self.assertEqual(user.email, old_primary)

    def test_maintain_verification_state(self):
        """
        For security reasons, the state of verification of the user email
        should be the same as it is when it is transferred into SecondaryEmail
        """

        old_primary = self.user.email
        self.user.is_active = False
        self.user.save()
        secondary_email = SecondaryEmailFactory(user=self.user)
        activation = ActivationProfile.objects.get(user=self.user,
                                                   email=secondary_email.email)
        ActivationProfile.objects.activate_user(activation.activation_key)
        secondary_email = SecondaryEmail.objects.get(user=self.user,
                                                     email=secondary_email.email)
        new_primary = secondary_email.email
        secondary_email.set_as_primary()

        old_email = SecondaryEmail.objects.get(email=old_primary)
        self.assertFalse(old_email.verified)
        user = User.objects.get(email=new_primary)

    def test_same_secondary_email(self):
        """
        All emails are unique. If an email is used as a user's primary email or
        another secondary email, it may not be used as a secondary email again.
        """
        secondary_email = SecondaryEmailFactory(user=self.user)
        with self.assertRaises(IntegrityError):
            new_secondary_email = SecondaryEmailFactory(user=self.user)
        new_secondary_email = SecondaryEmailFactory(user=self.user,
                                                    email='email@example.com')

    def test_delete_secondary_email(self):
        """
        Deleting a secondary email should also delete its activation profile
        """
        self.assertEqual(ActivationProfile.objects.count(), 0)
        secondary_email = SecondaryEmailFactory(user=self.user)
        self.assertEqual(ActivationProfile.objects.count(), 1)
        secondary_email.delete()
        self.assertEqual(ActivationProfile.objects.count(), 0)

    def test_add_military_service(self):
        military_service = MilitaryServiceFactory(user=self.user)
        military_service.save()

        ms_object = ProfileUnits.objects.filter(
            content_type__name="military service").count()
        self.assertEqual(ms_object, 1)
        
    def test_add_license(self):
        license_form = LicenseFactory(user=self.user)
        license_form.save()

        ms_object = ProfileUnits.objects.filter(
            content_type__name="license").count()
        self.assertEqual(ms_object, 1)

    def test_add_website(self):
        website_instance = WebsiteFactory(user=self.user)
        website_instance.save()

        ms_object = ProfileUnits.objects.filter(
            content_type__name="website").count()
        self.assertEqual(ms_object, 1)

    def test_add_summary(self):
        summary_instance = SummaryFactory(user=self.user)
        summary_instance.save()

        ms_object = ProfileUnits.objects.filter(
            content_type__name="summary").count()
        self.assertEqual(ms_object, 1)

    def test_add_volunteer_history(self):
        vh_instance = VolunteerHistoryFactory(user=self.user)
        vh_instance.save()

        ms_object = ProfileUnits.objects.filter(
            content_type__name="volunteer history").count()
        self.assertEqual(ms_object, 1)
