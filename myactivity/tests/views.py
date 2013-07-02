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
from myprofile.tests.factories import PrimaryNameFactory

EMPLOYER = Group.objects.get(name='Employer')
SEARCH_OPTS = ['django', 'python', 'programming']

class MyActivityViewsTests(TestCase):
    def setUp(self):
        self.staff_user = UserFactory()
        self.staff_user.groups.add(EMPLOYER)
        self.staff_user.save()

        self.client = TestClient()
        self.client.login_user(self.staff_user)

        self.candidate_user = UserFactory(email="example@example.com")
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
        self.assertEqual(len(soup.select('#search-table tr')), 29)
        self.assertEqual(len(soup.select('#user-table tr')), 10)

    def test_candidate_has_opted_in(self):
        response = self.client.post(reverse('candidate_information', kwargs={'user_id':'2'}))

        self.assertEqual(response.status_code, 200)

    def test_candidate_has_opted_out(self):
        self.candidate_user.opt_in_employers = False
        self.candidate_user.save()

        try:
            response = self.client.post(reverse('candidate_information', kwargs={'user_id':'2'}))
        except DoesNotExist:
            self.assertEqual(response.status_code, 404)
