from django.test import TestCase

from myjobs.forms import ChangePasswordForm, EditAccountForm
from myjobs.models import User
from myjobs.tests.factories import UserFactory
from myprofile.tests.factories import PrimaryNameFactory
from myprofile.models import Name

class AccountFormTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.name = PrimaryNameFactory(user=self.user)
        
    def test_password_form(self):
        invalid_data = [
            { 'data': {'password1': 'cats',
                       'password2': 'dogs',
                       'new_password': 'newpassword'},
              'error': ('password1', [u"Wrong password."])},
            { 'data': {'password1': 'secret',
                       'password2': 'dogs',
                       'new_password': 'newpassword'},
              'error': ('__all__', [u"The two password fields didn't match."])}]

        for item in invalid_data:
            form = ChangePasswordForm(user=self.user, data=item['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[item['error'][0]],
                             item['error'][1])

        form = ChangePasswordForm(user=self.user,data={'password1': 'secret',
                                                       'password2': 'secret',
                                                       'new_password': 'anothersecret'})
        
        self.failUnless(form.is_valid())
        form.save()
        self.failUnless(self.user.check_password('anothersecret'))

    def test_no_name_account_form(self):
        """
        Leaving both the first and last name fields blank produces a valid save.
        It also deletes the primary name object from the Name model.
        """
        data = {"gravatar": "alice@example.com", "user": self.user}
        form = EditAccountForm(data, **{'user':self.user})
        self.assertTrue(form.is_valid())
        form.save(self.user)
        self.assertEqual(Name.objects.count(), 0) 

    def test_both_names_account_form(self):
        """
        Filling out both name fields produces a valid save.
        """
        
        data = {"given_name": "Alicia", "family_name": "Smith",
                "gravatar": "alice@example.com"}
        form = EditAccountForm(data, **{'user':self.user})
        self.assertTrue(form.is_valid())

    def test_partial_name_account_form(self):
        """
        Filling out only the first name or only the last name produces an error.
        """
        data = {"given_name": "Alicia", "gravatar": "alice@example.com",
                "user": self.user}
        form = EditAccountForm(data, **{'user':self.user})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors()[0],
                         "You must enter both a first and last name.")
