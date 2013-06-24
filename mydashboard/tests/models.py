from django.test import TestCase

from mydashboard.models import *
from mydashboard.tests.factories import CompanyFactory
from mydashboard.tests.test_forms import CompanyUserForm
from myjobs.models import User
from myjobs.tests.factories import UserFactory

class CompanyUserTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.company = CompanyFactory()
        self.data = {'user': self.user.id,
                     'company': self.company.id}

    def test_add_admin(self):
        """
        Adding a user as an admin results in that user being added to
        the Employer group. Attempting to add that user as an admin to the
        same company again results in the form being invalidated.
        """
        company_user_form = CompanyUserForm(data=self.data)
        self.assertTrue(company_user_form.is_valid())
        company_user_form.save()

        self.user = User.objects.get(email=self.user.email)
        self.assertTrue(CompanyUser.GROUP in self.user.groups.all())

        company_user_form = CompanyUserForm(data=self.data)
        self.assertFalse(company_user_form.is_valid())

        self.assertEqual(company_user_form.errors['__all__'][0],
                         'Company user with this User and Company already exists.')

    def test_add_admin_multiple_companies(self):
        """
        If a user is an admin for multiple companies, the user's Employer group
        membership will not be revoked until that user's admin status has been
        revoked for all of those companies.
        """
        company2 = CompanyFactory(id=2)

        company_user = CompanyUser.objects.create(user=self.user,
                                      company=self.company)
        company_user_2 = CompanyUser.objects.create(user=self.user,
                                              company=company2)

        self.assertTrue(CompanyUser.GROUP in self.user.groups.all())

        company_user.delete()
        self.assertTrue(CompanyUser.GROUP in self.user.groups.all())

        company_user_2.delete()
        self.assertTrue(CompanyUser.GROUP not in self.user.groups.all())
