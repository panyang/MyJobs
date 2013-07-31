from django.http import Http404


def user_is_allowed(function):
    """
    Decorator; Ensures that the requested user has permission to
    access the decorated view. The wrapped function must accept an HttpRequest
    object as its first parameter and an additional keyword argument,
    :user_email:, at the very least.
    """
    def wrap(request, *args, **kwargs):
        if (request.user.is_anonymous() or
                request.user.email == kwargs.get('user_email')):
            return function(request, *args, **kwargs)
        raise Http404

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
