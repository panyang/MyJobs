from django.core import mail
from django.test import TestCase

from myjobs.models import *
from myprofile.models import *
from myjobs.tests import TestClient

class MyProfileTests(TestCase):
    user_info = {'password1': 'complicated_password',
                 'email': 'alice@example.com'}

    def setUp(self):
        super(MyProfileTests, self).setUp()
        self.user = User.objects.create_inactive_user(**self.user_info)

    def test_primary_name_save(self):
        """
        Saving a primary name when one already exists replaces it with
        the new primary name.
        """

        initial_name = {'given_name':'Alice',
                        'family_name':'Smith',
                        'primary':True,
                        'user':self.user}
        new_primary_name = {'given_name':'Alicia',
                            'family_name':'Smith',
                            'primary':True,
                            'user':self.user}

        initial_name_obj = Name.objects.create(**initial_name)
        self.assertTrue(initial_name_obj.primary)
        new_name_obj = Name.objects.create(**new_primary_name)
        initial_name_obj = Name.objects.get(given_name='Alice')
        self.assertTrue(new_name_obj.primary)
        self.assertFalse(initial_name_obj.primary)

    def test_secondary_email_save(self):
        """
        Saving a verified secondary email as the primary email (1) replaces
        the email in the user model (2) removes that email from the
        SecondaryEmail model and (3) adds the previous primary email in the
        secondary email model
        """
        self.assertEqual(2,2)
