from functools import wraps
import logging

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from myjobs.models import User

logger = logging.getLogger(__name__)


def user_is_allowed(model=None, pk_name=None, keep_email=False):
    """
    Determines if the currently logged in user should be accessing the
    decorated view

    Expects that the url contains a captured `user_email` parameter that is
    not vital to view functionality; This is removed from the view's kwargs
    and is not passed to the view itself unless the decorator is provided with
    a `keep_email` parameter.

    Logs a warning if `user_email` is not provided or is empty. This could be
    an indicator of two things:
    - Using this decorator may not be necessary
    - If using this decorator really is desired, the url pattern may not be
        set up correctly

    Inputs:
    :model: Optional; Model class that the user is trying to access
    :pk_name: Optional; Name of the id parameter being passed to
        the decorated view
    :keep_email: Optional; Denotes whether or not email should be passed to
        the decorated view

    Outputs:
    :response: Http404 or the results of running the decorated view
    """
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            try:
                if keep_email:
                    email = kwargs['user_email']
                else:
                    email = kwargs.pop('user_email')
            except KeyError:
                logger.warning('`user_is_allowed` decorator used, but '
                               'no email provided')
                email = None

            if not request.user.is_anonymous():
                if ((not email or
                     request.user != User.objects.get_email_owner(email))):
                    # If the currently logged in user doesn't own the email
                    # address from the requested url or no email address is
                    # provided, log out the user and redirect to home page
                    logout(request)
                    raise Http404

            if pk_name:
                pk = kwargs.get(pk_name)
                if pk:
                    try:
                        pk = int(pk)
                        # If the current user doesn't own the requested object
                        # or said object does not exist, redirect to 404 page
                        obj = get_object_or_404(model.objects,
                                                user=request.user,
                                                id=pk)
                    except ValueError:
                        # The value may not be an int; Saved searches, for
                        # example, pass 'digest' when working with digests
                        pass

            # Everything passed; Continue to the desired view
            return view_func(request, *args, **kwargs)
        return wraps(view_func)(wrap)
    return decorator
