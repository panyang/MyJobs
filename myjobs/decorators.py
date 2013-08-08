from functools import wraps

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from myjobs.models import User

def user_is_allowed(model=None, pk_name=None):
    """
    Determines if the currently logged in user should be accessing the
    decorated view

    Expects that the url contains a captured `user_email` parameter that is
    not vital to view functionality; This is removed from the view's kwargs
    and is not passed to the view itself.

    Throws KeyError if email is not provided. This is an indicator of two
    things:
    - Using this decorator may not be necessary
    - If using this decorator really is desired, the url pattern may not be
        set up correctly

    Inputs:
    :model: Optional; Model class that the user is trying to access
    :pk_name: Optional; Name of the id parameter being passed to
        the decorated view

    Outputs:
    :response: Http404 or the results of running the decorated view
    """
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            email = kwargs.pop('user_email')

            if not request.user.is_anonymous():
                if request.user != User.objects.get_email_owner(email):
                    # If the currently logged in user doesn't own the email
                    # address from the requested url, log out the user
                    # and redirect to home page
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
