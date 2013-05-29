from django.contrib.auth.backends import ModelBackend

from myjobs.models import User


class CaseInsensitiveAuthBackend(ModelBackend):
    """
    We modify the user's email address when accounts are created.

    This causes issues if our modification is different than what
    the user typed  in.

    Override ModelBackground's `authenticate` method to allow for
    case-insensitive login
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
