from bs4 import BeautifulSoup
from importlib import import_module
import json

from django.conf import settings
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory
from myprofile.models import *
from myprofile.views import *
from myprofile.tests.factories import *

class MyProfileViewsTests(TestCase):
    def setUp(self):
        super(MyProfileViewsTests, self).setUp()
        self.user = UserFactory()
        self.client = TestClient()
        self.client.login_user(self.user)
        self.name = PrimaryNameFactory(user=self.user)

    def test_edit_profile(self):
        """
        Going to the edit_profile view generates a list of existing profile
        items in the main content section and a list of profile sections that
        don't have data filled out in the sidebar.
        """
        resp = self.client.get(reverse('view_profile'))
        soup = BeautifulSoup(resp.content)
        item_id = Name.objects.all()[0].id

        # The existing name object should be rendered on the main content section
        self.assertIsNotNone(soup.find('tr', id='Name-'+str(item_id)+'-item'))
        # profile-section contains the name of a profile section that has no
        # information filled out yet and shows up in the sidebar
        self.assertTrue(soup.findAll('tr',{'class':'profile-section'}))
        
    def test_handle_form_get_new(self):
        """
        Invoking the handle_form view without an id parameter returns an
        empty form with the correct form id
        """

        resp = self.client.get(reverse('handle_form'),
                               data = {'module': 'Name'})
        self.assertTemplateUsed(resp, 'myprofile/profile_form.html')
        soup = BeautifulSoup(resp.content)
        self.assertEquals(soup.form.attrs['id'], 'profile-unit-form')
        with self.assertRaises(KeyError):
            soup.find('input', id='id_name-given_name').attrs['value']

    def test_handle_form_get_existing(self):
        """
        Invoking the handle_form view with and id paraemeter returns
        a form filled out with the corresponding profile/ID combination
        """
        
        resp = self.client.get(reverse('handle_form'),
                               data = {'module': 'Name', 'id': self.name.id})
        self.assertTemplateUsed(resp, 'myprofile/profile_form.html')
        soup = BeautifulSoup(resp.content)
        self.assertEquals(soup.form.attrs['id'], 'profile-unit-form')
        self.assertEquals(soup.find('input', id='id_name-given_name')
                          .attrs['value'], 'Alice')
        self.assertEquals(soup.find('input', id='id_name-family_name')
                          .attrs['value'], 'Smith')
        self.assertEquals(soup.find('input', id='id_name-primary')
                          .attrs['checked'], 'checked')

    def test_handle_form_post_new_valid(self):
        """
        Invoking the handle_form view as a POST request for a new item
        creates that object in the database and returns the item snippet
        to be rendered on the page.
        """

        resp = self.client.post(reverse('handle_form'),
                               data = {'module': 'Name', 'id': 'new',
                                       'given_name': 'Susy',
                                       'family_name': 'Smith'
                                   })
        self.assertRedirects(resp, reverse('view_profile'))
        self.assertEqual(Name.objects.filter(given_name='Susy',
                                             family_name='Smith').count(), 1)

    def test_handle_form_post_invalid(self):
        """
        Invoking the handle_form view as a POST request with an invalid
        form returns the list of form errors.
        """
        resp = self.client.post(reverse('handle_form'),
                                data = {'module': 'Name', 'id': 'new',
                                        'given_name': 'Susy'},
                                HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')

        self.assertEqual(json.loads(resp.content),
            {u'family_name': [u'This field is required.']})

    def test_handle_form_post_existing_valid(self):
        """
        Invoking the handle_form view as a POST request for an existing
        item updates that item and returns the update item snippet.
        """
        resp = self.client.post(reverse('handle_form'),
                               data = {'module': 'Name', 'id': self.name.id,
                                       'given_name': 'Susy',
                                       'family_name': 'Smith'})
        self.assertRedirects(resp, reverse('view_profile'))
        self.assertEqual(Name.objects.filter(given_name='Susy',
                                             family_name='Smith').count(), 1)

    def test_delete_item(self):
        """
        Invoking the delete_item view deletes the item and returns
        the 'Deleted!' HttpResponse
        """

        resp = self.client.post(reverse('delete_item', args=[self.name.id]))

        self.assertEqual(resp.content, '')
        self.assertEqual(Name.objects.filter(id=self.name.id).count(), 0)

    def test_add_duplicate_primary_email(self):
        """
        Attempting to add a secondary email with a value equal to the user's
        current primary email results in an error.

        Due to how the instance is constructed, this validation is form-level
        rather than model-level.
        """
        resp = self.client.post(reverse('handle_form'),
                                data = {'module': 'SecondaryEmail',
                                        'id': 'new',
                                        'email': self.user.email},
                                HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(json.loads(resp.content),
            {u'email': [u'This email is already registered.']})
