from myjobs.models import User
from myjobs import forms
from django.test import TestCase

class ChangePasswordForm(TestCase):
    def test_password_form(self):
        user=User.objects.create_user(**{'email':'alice@example.com', 'password1':'secret'})
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
            form = forms.ChangePasswordForm(user=user, data=item['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[item['error'][0]],
                             item['error'][1])

        form = forms.ChangePasswordForm(user=user,data={'password1': 'secret',
                                            'password2': 'secret',
                                            'new_password': 'anothersecret'})
        
        self.failUnless(form.is_valid())
        form.save(user)
        self.failUnless(user.check_password('anothersecret'))
