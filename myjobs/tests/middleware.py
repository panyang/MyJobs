import urllib

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import RequestFactory

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


    def __init__(self, user=AnonymousUser()):
        self.user = user
        if user.is_anonymous():
            email = 'email@example.com'
        else:
            email = self.user.email
        self.path = reverse('edit_account', args=[email])
        quoted_email = urllib.quote(email)
        self.REQUEST = {'next': '?next=/%s//account/'
                            % [quoted_email]}


class RedirectMiddlewareTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.redirect_middleware = RedirectMiddleware()
        self.request_factory = RequestFactory()

    def test_logged_in_no_redirect(self):
        """
        A logged in user whose password_change flag is not set
        should proceed to their original destination
        """
        request = self.request_factory.get(reverse('edit_account',
                                                   args=[self.user.email]))
        request.user = self.user
        response = self.redirect_middleware.process_request(request)
        self.assertEqual(response, None)

    def test_logged_in_autocreated_user_redirects(self):
        """
        A logged in user whose password_change flag is set should
        be redirected to the password change form
        """
        self.user.password_change = True
        self.user.save()

        request = self.request_factory.get(reverse('saved_search_main',
                                                   args=[self.user.email]))
        request.user = self.user

        response = self.redirect_middleware.process_request(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'),
                         reverse('edit_account',
                                 args=[self.user.email]))

    def test_not_logged_in_returns_forbidden(self):
        """
        An anonymous user that tries to post to a private url should
        receive a 403 Forbidden status
        """
        #request = self.client.get(reverse('saved_search_main',
        #                                  args=[self.user.email]))
        request = self.request_factory.get(reverse('saved_search_main',
                                                   args=[self.user.email]),
                                                   HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        new_request = request.GET.copy()
        new_request['next'] = reverse('home')
        request.GET = new_request
        request.REQUEST.dicts = (new_request, request.POST)
        request.user = AnonymousUser()
        response = self.redirect_middleware.process_request(request)
        self.assertEqual(response.status_code, 403)
