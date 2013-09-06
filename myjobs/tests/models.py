import urllib
from django.contrib.auth.models import Group
from django.core import mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase
from django.utils.http import urlquote

from myjobs.models import *
from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory


class UserManagerTests(TestCase):
    user_info = {'password1': 'complicated_password',
                 'email': 'alice@example.com'}

    def test_inactive_user_creation(self):
        new_user, created = User.objects.create_inactive_user(**self.user_info)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_active, False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))
        self.failUnless(new_user.groups.filter(name='Job Seeker').count() == 1)
        self.assertIsNotNone(new_user.user_guid)
        print new_user.user_guid

    def test_active_user_creation(self):
        new_user = User.objects.create_user(**self.user_info)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))
        self.failUnless(new_user.groups.filter(name='Job Seeker').count() == 1)
        self.assertIsNotNone(new_user.user_guid)

    def test_superuser_creation(self):
        new_user = User.objects.create_superuser(
            **{'password': 'complicated_password',
               'email': 'alice@example.com'})
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_superuser, True)
        self.assertEqual(new_user.is_staff, True)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))
        self.failUnless(new_user.groups.filter(name='Job Seeker').count() == 1)
        self.assertIsNotNone(new_user.user_guid)

    def test_gravatar_url(self):
        """
        Test that email is hashed correctly and returns a 200 response
        """
        user = UserFactory()
        static_gravatar_url = "http://www.gravatar.com/avatar/c160f8cc69a4f0b" \
                              "f2b0362752353d060?s=20&d=mm"
        generated_gravatar_url = user.get_gravatar_url()
        self.assertEqual(static_gravatar_url, generated_gravatar_url)
        status_code = urllib.urlopen(static_gravatar_url).getcode()
        self.assertEqual(status_code, 200)

    def test_not_disabled(self):
        """
        An anonymous user who provides the :verify-email: query string or
        user with is_disabled set to True should be redirected to the home
        page. An anonymous user who does not should see a 404. A user with
        is_active set to False should proceed to their destination.
        """
        client = TestClient()
        user = UserFactory()

        #Anonymous user
        resp = client.get(reverse('view_profile'))
        self.assertRedirects(resp, reverse('home'))

        # This is ugly, but it is an artifact of the way Django redirects
        # users who fail the `user_passes_test` decorator.
        qs = '?verify-email=%s' % user.email
        next_qs = '?next=' + urlquote('/profile/view/%s' % qs)

        # Anonymous user navigates to url with :verify-email: in query string
        resp = client.get(reverse('view_profile') + qs)
        # Old path + qs is urlquoted and added to the url as the :next: param
        self.assertRedirects(resp, "http://testserver/" + next_qs)

        # Active user
        client.login_user(user)
        resp = client.get(reverse('view_profile'))
        self.assertTrue(resp.status_code, 200)

        #Disabled user
        user.is_disabled = True
        user.save()
        resp = client.get(reverse('view_profile'))
        self.assertRedirects(resp, "http://testserver/?next=/profile/view/")

    def test_is_active(self):
        """
        A user with is_active set to False should be redirected to the home
        page, while a user with is_active set to True should proceed to their
        destination.
        """
        client = TestClient()
        user = UserFactory()
        quoted_email = urllib.quote(user.email)

        # Active user
        client.login_user(user)
        resp = client.get(reverse('saved_search_main'))
        self.assertTrue(resp.status_code, 200)

        # Inactive user
        user.is_active = False
        user.save()
        resp = client.get(reverse('saved_search_main'))
        self.assertRedirects(resp, "http://testserver/?next=/saved-search/view/")

    def test_group_status(self):
        """
        Should return True if user.groups contains the group specified and
        False if it does not.
        """
        client = TestClient()
        user = UserFactory()

        user.groups.all().delete()

        for group in Group.objects.all():
            # Makes a list of all group names, excluding the one that the
            # user will be a member of
            names = map(lambda group: group.name,
                        Group.objects.filter(~Q(name=group.name)))

            user.groups.add(group.pk)
            user.save()

            for name in names:
                self.assertFalse(User.objects.is_group_member(user, name))
            self.assertTrue(User.objects.is_group_member(user, group.name))

            user.groups.all().delete()
