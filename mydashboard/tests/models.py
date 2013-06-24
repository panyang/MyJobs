from django.test import TestCase

from mydashboard.models import *
from mydashboard.tests.factories import CompanyFactory
from mydashboard.tests.test_forms import AdministratorsForm
from myjobs.models import User
from myjobs.tests.factories import UserFactory

class AdministratorsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.company = CompanyFactory()
        self.data = {'admin': self.user.id,
                     'company': self.company.id}

    def test_add_admin(self):
        """
        Adding a user as an administrator results in that user being added to
        the Staff group. Attempting to add that user as an administrator to the
        same company again results in the form being invalidated.
        """
        admin_form = AdministratorsForm(data=self.data)
        self.assertTrue(admin_form.is_valid())
        admin_form.save()

        self.user = User.objects.get(email=self.user.email)
        self.assertTrue(Administrators.ADMIN_GROUP in self.user.groups.all())

        admin_form = AdministratorsForm(data=self.data)
        self.assertFalse(admin_form.is_valid())

        self.assertEqual(admin_form.errors['__all__'][0],
                         'Administrator with this Admin and Company already exists.')

    def test_add_admin_multiple_companies(self):
        """
        If a user is an admin for multiple companies, the user's Staff group
        membership will not be revoked until that user's admin status has been
        revoked for all of those companies.
        """
        company2 = CompanyFactory(id=2)

        admin = Administrators.objects.create(admin=self.user,
                                      company=self.company)
        admin2 = Administrators.objects.create(admin=self.user,
                                              company=company2)

        self.assertTrue(Administrators.ADMIN_GROUP in self.user.groups.all())

        admin.delete()
        self.assertTrue(Administrators.ADMIN_GROUP in self.user.groups.all())

        admin2.delete()
        self.assertTrue(Administrators.ADMIN_GROUP not in self.user.groups.all())
