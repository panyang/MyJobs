from django.test import TestCase

from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory

from mysearches import forms

class MySearchViewTests(TestCase):
    def setUp(self):
        super(MySearchViewTests, self).setUp()
        self.client = TestClient()
        self.user = UserFactory()
        self.client.login_user(self.user)

    def test_search_main(self):
        response = self.client.get('/saved-search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysearches/saved_search_main.html')
        self.assertTemplateUsed(response, 'includes/form-error-highlight.html')
        self.failUnless(isinstance(response.context['form'], forms.DigestForm));
        self.failUnless(isinstance(response.context['add_form'],
                        forms.SavedSearchForm));
