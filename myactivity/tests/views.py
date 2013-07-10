from bs4 import BeautifulSoup
from datetime import timedelta
import random

from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import TestCase

from myjobs.models import User
from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory
from mysearches.models import SavedSearch
from mysearches.tests.factories import SavedSearchFactory
from myprofile.models import ProfileUnits
from myprofile.tests.factories import PrimaryNameFactory, SecondaryEmailFactory, EducationFactory
from myprofile.tests.factories import AddressFactory, TelephoneFactory, EmploymentHistoryFactory
from mydashboard.tests.factories import CompanyFactory, CompanyUserFactory, MicrositeFactory


EMPLOYER = Group.objects.get(name='Employer')
SEARCH_OPTS = ['django', 'python', 'programming']

class MyActivityViewsTests(TestCase):
    def setUp(self):
        self.staff_user = UserFactory()
        self.staff_user.groups.add(EMPLOYER)
        self.staff_user.save()

        self.company = CompanyFactory()
        self.company.save()
        self.admin = CompanyUserFactory(user=self.staff_user, company=self.company)
        self.admin.save()
        self.microsite = MicrositeFactory(company=self.company)
        self.microsite.save()

        self.client = TestClient()
        self.client.login_user(self.staff_user)

        self.candidate_user = UserFactory(email="example@example.com")
        SavedSearchFactory(user=self.candidate_user, 
                           url='test.jobs/search?q=django', 
                           label='test Jobs')
        self.candidate_user.save()

        for i in range(10):
            # Create 50 new users
            user = UserFactory(email='example%s@example.com'%i)
            for search in SEARCH_OPTS:
                # Create 150 new searches and assign three per user
                SavedSearchFactory(user=user,
                                   url='indiana.jobs/search?q=%s'%search,
                                   label='%s Jobs'%search)

    def test_number_of_searches_and_users_is_correct(self):
        response = self.client.get(reverse('activity_search_feed'))
        response = self.client.post(reverse('activity_search_feed'),
                                    {'microsite':'indiana.jobs'})
        soup = BeautifulSoup(response.content)
        self.assertEqual(len(soup.select('#search-table tr')), 30)
        self.assertEqual(len(soup.select('#user-table tr')), 10)

        old_search = SavedSearch.objects.all()[0]
        old_search.created_on -= timedelta(days=8)
        old_search.save()

        response = self.client.post(reverse('activity_search_feed'),
                                    {'microsite':'indiana.jobs'})
        soup = BeautifulSoup(response.content)
        self.assertEqual(len(soup.select('#search-table tr')), 30)
        self.assertEqual(len(soup.select('#user-table tr')), 10)

    # Eventually these opted-in/out will be changed to 
    # track if user is part of company's activity feed
    def test_candidate_has_opted_in(self):
        response = self.client.post(reverse('candidate_information', kwargs={'user_id':self.candidate_user.id}))

        self.assertEqual(response.status_code, 200)

    def test_candidate_has_opted_out(self):
        self.candidate_user.opt_in_employers = False
        self.candidate_user.save()

        response = self.client.post(reverse('candidate_information', kwargs={'user_id':self.candidate_user.id}))
        self.assertEqual(response.status_code, 404)

    def test_candidate_page_load_with_profileunits_and_activites(self):
        # Building User with ProfileUnits
        self.name = PrimaryNameFactory(user = self.candidate_user)
        self.second_email = SecondaryEmailFactory(user = self.candidate_user)
        self.education = EducationFactory(user = self.candidate_user)
        self.address = AddressFactory(user = self.candidate_user)
        self.telephone = TelephoneFactory(user = self.candidate_user)
        self.employment = EmploymentHistoryFactory(user = self.candidate_user)
        self.candidate_user.save()

        response = self.client.post(reverse('candidate_information', kwargs={'user_id':self.candidate_user.id}))

        soup = BeautifulSoup(response.content)
        titles = soup.find('div', {'id':'candidate-content'}).findAll('a', {'class':'accordion-toggle'})
        info = soup.find('div', {'id':'candidate-content'}).findAll('li')

        self.assertEqual(len(titles), 6)
        self.assertEqual(len(info), 16)
        self.assertEqual(response.status_code, 200)

    def test_candidate_page_load_without_profileunits_with_activites(self):
        response = self.client.post(reverse('candidate_information', kwargs={'user_id':self.candidate_user.id}))

        soup = BeautifulSoup(response.content)
        titles = soup.find('div', {'id':'candidate-content'}).findAll('a', {'class':'accordion-toggle'})
        info = soup.find('div', {'id':'candidate-content'}).findAll('li')

        self.assertEqual(len(titles), 1)
        self.assertEqual(len(info), 3)
        self.assertEqual(response.status_code, 200)

    def test_candidate_page_load_without_profileunits_and_activites(self):
        saved_search = SavedSearch.objects.get(user=self.candidate_user)
        saved_search.delete()
        response = self.client.post(reverse('candidate_information', kwargs={'user_id':self.candidate_user.id}))

        soup = BeautifulSoup(response.content)
        info = soup.find('div', {'id':'candidate-content'})

        self.assertFalse(info)
        self.assertEqual(response.status_code, 404)
