from functools import wraps

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from myjobs.models import User


def user_is_allowed(model=None, pk_name=None, pass_user=False):
    """
    Determines if the currently logged in user should be accessing the
    decorated view

    Expects that the query string contains a :verify-email: key if the
    request originates from a My.Jobs email; The user using this address
    is added to the view's kwargs as :user: if :pass_user: is True. If the
    user is not anonymous, passing :verify-email: will ensure that the user
    owns that address.

    Inputs:
    :model: Optional; Model class that the user is trying to access
    :pk_name: Optional; Name of the id parameter being passed to
        the decorated view
    :pass_user: Optional; Denotes whether or not the email's owner should be
        passed to the decorated view

    Outputs:
    :response: Http404 or the results of running the decorated view

    GET Parameters:
    :verify-email: Optional; User's primary email; Ensures that an individual
        is authorized to access a logged in user's information
    """
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            email = request.GET.get('verify-email', '')
            user = User.objects.get_email_owner(email)
            if request.user.is_anonymous() and not email:
                return HttpResponseRedirect(reverse('home'))

            if email:
                user = User.objects.get_email_owner(email)
                if not user:
                    # :verify-email: was provided but no user exists
                    # Log out the user and redirect to login page
                    logout(request)
                    return HttpResponseRedirect(reverse('home'))

            if not request.user.is_anonymous():
                if user:
                    if request.user != user:
                        # If the currently logged in user doesn't own the
                        # provided email address, log out the user and
                        # redirect to login page
                        logout(request)
                        return HttpResponseRedirect(reverse('home'))
                else:
                    # If user was not set previously, set it to the currently
                    # logged in user.
                    user = user or request.user

            if pass_user:
                # If :pass_user: is provided, the email address owner should be
                # passed to the decorated view.
                kwargs['user'] = user

            if pk_name:
                pk = request.REQUEST.get(str(pk_name))
                if pk:
                    try:
                        pk = int(pk)
                        # If the current user doesn't own the requested object
                        # or said object does not exist, redirect to 404 page
                        obj = get_object_or_404(model.objects,
                                                user=user,
                                                id=pk)
                    except ValueError:
                        # The value may not be an int; Saved searches, for
                        # example, pass 'digest' when working with digests
                        pass

            # Everything passed; Continue to the desired view
            return view_func(request, *args, **kwargs)
        return wraps(view_func)(wrap)
    return decorator
