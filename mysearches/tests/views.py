from django.test import TestCase
import json

from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory

from mysearches import forms
from mysearches import models
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
        }
        self.new_digest_data = {
            'is_active': 'True',
            'user': self.user,
            'email': self.user.email,
        }
        self.new_form = forms.SavedSearchForm(user=self.user,
                                         data=self.new_form_data)

    def test_search_main(self):
        response = self.client.get('/saved-search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_main.html')
        self.assertTemplateUsed(response, 'includes/form-error-highlight.html')
        self.failUnless(isinstance(response.context['form'], forms.DigestForm));
        self.failUnless(isinstance(response.context['add_form'],
                        forms.SavedSearchForm));

    def test_save_new_search_form(self):
        response = self.client.post('/saved-search/new',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'success')

        del self.new_form_data['feed']
        del self.new_form_data['frequency']
        response = self.client.post('/saved-search/new',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), ['feed', 'frequency'])

    def test_get_edit_template(self):
        self.new_form.save()
        search_id = self.new_form.instance.id
        response = self.client.post('/saved-search/edit',
                                    data = {'search_id': search_id,},
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.new_form.instance,
                         response.context['form'].instance)
        self.assertTemplateUsed(response, 'mysearches/saved_search_edit.html')

        search_id += 1
        response = self.client.post('/saved-search/edit',
                                    data = {'search_id': search_id,},
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_edit.html')
        self.assertEqual(response.context['form'].instance, models.SavedSearch())

    def test_save_edit_form(self):
        self.new_form.save()
        search_id = self.new_form.instance.id

        self.new_form_data['frequency'] = 'W'
        self.new_form_data['day_of_week'] = 1
        self.new_form_data['search_id'] = search_id

        response = self.client.post('/saved-search/save-edit',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'success')

        del self.new_form_data['frequency']
        self.new_form_data['search_id'] = search_id

        response = self.client.post('/saved-search/save-edit',
                                    data = self.new_form_data,
                                    HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), ['frequency'])

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

    def test_delete_digest_form(self):
        def delete():
            response = self.client.post('/saved-search/delete-digest',
                                        HTTP_X_REQUESTED_WITH =
                                            'XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, 'success')

        delete()

        digest = SavedSearchDigestFactory(user=self.user)
        delete()
