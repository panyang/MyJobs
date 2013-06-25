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

    def test_add_company_user(self):
        """
        Adding one user as a company user multiple times returns an error
        message.
        """
        company_user_form = CompanyUserForm(data=self.data)
        self.assertTrue(company_user_form.is_valid())
        company_user_form.save()

        self.assertEqual(self.company.admins.count(), 1)

        company_user_form = CompanyUserForm(data=self.data)
        self.assertFalse(company_user_form.is_valid())

        self.assertEqual(company_user_form.errors['__all__'][0],
                         'Company user with this User and Company already exists.')
