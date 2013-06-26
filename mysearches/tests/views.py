from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.test import TestCase
import json

from testfixtures import Replacer

from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory

from mysearches import forms
from mysearches import helpers
from mysearches import models
from mysearches.tests.test_helpers import return_file
from mysearches.tests.factories import SavedSearchDigestFactory, SavedSearchFactory


class MySearchViewTests(TestCase):
    def setUp(self):
        super(MySearchViewTests, self).setUp()
        self.client = TestClient()
        self.user = UserFactory()
        self.client.login_user(self.user)
        self.new_form_data = {
            'url': 'jobs.jobs/jobs',
            'feed': 'http://jobs.jobs/jobsfeed/rss?',
            'label': 'Jobs Label',
            'email': self.user.email,
            'frequency': 'D',
            'is_active': 'True',
            'render': 'True',
        }
        self.new_digest_data = {
            'is_active': 'True',
            'user': self.user,
            'email': self.user.email,
        }
        self.new_form = forms.SavedSearchForm(user=self.user,
                                         data=self.new_form_data)
        
        self.r = Replacer()
        self.r.replace('urllib2.urlopen', return_file)

    def tearDown(self):
        self.r.restore()

    def test_search_main(self):
        response = self.client.get('/saved-search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_main.html')
        self.assertTemplateUsed(response, 'includes/form-error-highlight.html')
        self.failUnless(isinstance(response.context['form'], forms.DigestForm));
        self.failUnless(isinstance(response.context['add_form'],
                        forms.SavedSearchForm));

    def test_save_new_search_form(self):
        response = self.client.post('/saved-search/save',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.new_form_data['label'] in response.content)

    def test_save_new_search_invalid(self):
        del self.new_form_data['feed']
        del self.new_form_data['frequency']
        response = self.client.post('/saved-search/save',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).keys(),
                         ['feed', 'frequency'])

    def test_get_edit_template(self):
        self.new_form.save()
        search_id = self.new_form.instance.id
        response = self.client.get('/saved-search/edit',
                                    data = {'search_id': search_id},
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(self.new_form.instance,
                         response.context['form'].instance)
        self.assertTemplateUsed(response, 'mysearches/saved_search_edit.html')

        search_id += 1
        response = self.client.get('/saved-search/edit',
                                    data = {'search_id': search_id},
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_edit.html')
        self.assertEqual(response.context['form'].instance, models.SavedSearch())

    def test_save_edit_form(self):
        self.new_form.save()
        search_id = self.new_form.instance.id

        self.new_form_data['frequency'] = 'W'
        self.new_form_data['day_of_week'] = 1
        self.new_form_data['url'] = 'jobs.jobs/search?'
        self.new_form_data['search_id'] = search_id

        new_form = forms.SavedSearchForm(user=self.user,
                                         data=self.new_form_data)
        response = self.client.post('/saved-search/save',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.new_form_data['label'] in response.content)

        del self.new_form_data['frequency']

        response = self.client.post('/saved-search/save',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).keys(), ['frequency'])

    def test_validate_url(self):
        response = self.client.post('/saved-search/validate-url',
                                    data = { 'url': self.new_form_data['url'] },
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = { 'rss_url': 'http://jobs.jobs/jobs/feed/rss',
                 'feed_title': 'Jobs',
                 'url_status': 'valid' }
        self.assertEqual(json.loads(response.content), data)

        response = self.client.post('/saved-search/validate-url',
                                    data = { 'url': 'google.com' },
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content),
                         { 'url_status': 'not valid' })

    def test_save_digest_form(self):
        response = self.client.post('/saved-search/save-digest',
                                    self.new_digest_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'success')

        del self.new_digest_data['email']
        response = self.client.post('/saved-search/save-digest',
                                    self.new_digest_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'failure')

    def test_unsubscribe_owned_search(self):
        """
        Unsubscribing an owned saved search should result in
        that search being deactivated
        """
        search = SavedSearchFactory(user=self.user)
        self.assertTrue(search.is_active)

        response = self.client.get(reverse('unsubscribe',
                                           kwargs={'search_id':search.id}))
        search = models.SavedSearch.objects.get(id=search.id)
        self.assertFalse(search.is_active)
        self.assertTemplateUsed(response,
                                'mysearches/saved_search_disable.html')

    def test_unsubscribe_unowned_search(self):
        """
        Attempting to unsubscribe using a search that isn't yours
        should result in nothing happening to the search
        """
        user = UserFactory(email='test@example.com')
        search = SavedSearchFactory(user=user)

        response = self.client.get(reverse('unsubscribe',
                                           kwargs={'search_id':search.id}))
        search = models.SavedSearch.objects.get(id=search.id)
        self.assertTrue(search.is_active)

    def test_unsubscribe_digest(self):
        """
        Unsubscribing a saved search digest should result in all
        of the owner's saved searches being disabled
        """
        digest = SavedSearchDigestFactory(user=self.user)
        searches = []
        for url in ['jobs.jobs/search?q=python', 'jobs.jobs/search?q=django']:
            searches.append(SavedSearchFactory(url=url, user=self.user))

        for search in searches:
            self.assertTrue(search.is_active)

        response = self.client.get(reverse('unsubscribe',
                                           kwargs={'search_id':'digest'}))
        searches = list(models.SavedSearch.objects.all())
        for search in searches:
            self.assertFalse(search.is_active)
        self.assertTemplateUsed(response,
                                'mysearches/saved_search_disable.html')

    def test_delete_owned_search(self):
        search = SavedSearchFactory(user=self.user)
        self.assertEqual(models.SavedSearch.objects.count(), 1)

        response = self.client.get(reverse('delete_saved_search',
                                           kwargs={'search_id':search.id}))
        self.assertEqual(models.SavedSearch.objects.count(), 0)

    def test_delete_unowned_search(self):
        """
        Attempting to delete a search that isn't yours should
        result in nothing happening to the search
        """
        user = UserFactory(email='test@example.com')
        search = SavedSearchFactory(user=user)

        response = self.client.get(reverse('delete_saved_search',
                                           kwargs={'search_id':search.id}))
        self.assertEqual(models.SavedSearch.objects.count(), 1)

    def test_delete_owned_searches_by_digest(self):
        """
        Deleting with a saved search digest should result in
        all of the user's saved searches being deleted
        """
        digest = SavedSearchDigestFactory(user=self.user)
        searches = []
        for url in ['jobs.jobs/search?q=python', 'jobs.jobs/search?q=django']:
            searches.append(SavedSearchFactory(url=url, user=self.user))

        self.assertEqual(models.SavedSearch.objects.count(), 2)

        response = self.client.get(reverse('delete_saved_search',
                                           kwargs={'search_id':'digest'}))
        self.assertEqual(models.SavedSearch.objects.count(), 0)
