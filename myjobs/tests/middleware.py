from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from MyJobs.middleware import RedirectMiddleware
from myjobs.models import User
from myjobs.tests.factories import UserFactory


class MockRequest(object):
    """
    Mock request object used for testing RedirectMiddleware. Can be expanded
    to work for other middlewares by adding more attributes if necessary
    """
    def is_ajax(self):
        return True

    REQUEST = {'next': '?next=/saved-search/save-digest'}
    path = reverse('edit_communication')

    def __init__(self, user=AnonymousUser()):
        self.user = user


class RedirectMiddlewareTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.redirect_middleware = RedirectMiddleware()

    def test_logged_in_no_redirect(self):
        """
        A logged in user whose password_change flag is not set
        should proceed to their original destination
        """
        request = MockRequest(self.user)
        response = self.redirect_middleware.process_request(request)
        self.assertEqual(response, None)

    def test_logged_in_autocreated_user_redirects(self):
        """
        A logged in user whose password_change flag is set should
        be redirected to the password change form
        """
        self.user.password_change = True
        self.user.save()
        self.user = User.objects.get(email=self.user.email)

        request = MockRequest(self.user)
        response = self.redirect_middleware.process_request(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('edit_account'))

    def test_not_logged_in_returns_forbidden(self):
        """
        An anonymous user that tries to post to a private url should
        receive a 403 Forbidden status
        """
        request = MockRequest()
        response = self.redirect_middleware.process_request(request)
        self.assertEqual(response.status_code, 403)
