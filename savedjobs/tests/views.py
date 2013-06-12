from django.core.urlresolvers import reverse
from django.test import TestCase

from savedjobs.models import *
from myjobs.tests import TestClient
from myjobs.models import User


class SavedJobsViewTests(TestCase):
     
    def setUp(self):
        super(SavedJobsViewTests, self).setUp()
        self.client = TestClient()
        self.user = User.objects.create_user(**{'email':'alice@example.com',
                                                'password1':'secret'})
        self.uid = 363107
        self.source = 'http://jobs.jobs/oklahoma-city-ok/ap-mechanics/363107/job/'
        
    def test_unauthorized_microsite_save(self):
        resp = self.client.get('http://testserver%s' % '/save/microsite/')
        self.assertRedirects(resp, 'http://testserver/accounts/login/?next=/save/microsite/')

    def test_invalid_microsite_values_save(self):
        self.client.login_user(self.user)
        uid = 21382193719238
        source = 'http://garbage.jobs'
        resp = self.client.get('http://testserver/save/microsite/?uid=%s&source=%s' %
                               (uid, source))
        self.assertEqual(resp.content, 'Job Not Found')
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 0)

    def test_successful_microsite_save(self):
        self.client.login_user(self.user)
        resp = self.client.get('http://testserver/save/microsite/?uid=%s&source=%s' %
                               (self.uid, self.source))
        self.assertEqual(resp.content, 'Success')
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 1)
        
    def test_new_uid_microsite_joblisting(self):
        self.client.login_user(self.user)

        self.assertEqual(len(SavedJob.objects.filter(uid=self.uid)), 0)
        resp = self.client.get('http://testserver/save/microsite/?uid=%s&source=%s' %
                               (self.uid, self.source))
        self.assertEqual(resp.content, 'Success')
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 1)

    def test_duplicate_microsite_saved_job(self):
        self.client.login_user(self.user)

        resp = self.client.get('http://testserver/save/microsite/?uid=%s&source=%s' %
                               (self.uid, self.source))
        self.assertEqual(resp.content, 'Success')
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 1)

        resp = self.client.get('http://testserver/save/microsite/?uid=%s&source=%s' %
                               (self.uid, self.source))
        self.assertEqual(resp.content, 'Job already exists!')
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 1)

class ManualSavedJobsViewTests(TestCase):
    def setUp(self):
        super(ManualSavedJobsViewTests, self).setUp()
        self.client = TestClient()
        self.user = User.objects.create_user(**{'email':'alice@example.com',
                                                'password1':'secret'})
        
    def test_successful_add(self):
        self.client.login_user(self.user)
        # Establish as ajax request
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        resp = self.client.post(reverse('manual_job_save'),
                                data = { 'action': 'add',
                                         'title': 'Astronaut',
                                         'company': 'NASA' },
                                **kwargs)
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 1)

    def test_invalid_add(self):
        self.client.login_user(self.user)
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        resp = self.client.post(reverse('manual_job_save'),
                                data = { 'action': 'add',
                                         'title': 'Astronaut'},
                                **kwargs)
        self.assertEqual(len(SavedJob.objects.filter(user=self.user)), 0)
        self.failIf(resp.context['form'].is_valid())

