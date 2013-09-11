from hashlib import sha1
import hmac

from django.db import models

from myjobs.models import User


class AuthorizedClient(models.Model):
    """
    Represents the set of web sites (:site:) that have been authorized by a
    user (:user:) to use that user's account
    """
    user = models.ForeignKey(User)
    site = models.CharField(max_length=255)

    class Meta:
        unique_together = (('user', 'site'),)

    @staticmethod
    def create_key(user):
        """
        Creates the key used to determine whether a user is authenticated. The
        key is currently very simple, but this is easily changed.

        This should be stored in the user's session cookie.
        """
        return hmac.new(str(user.id),
                        digestmod=sha1).hexdigest()
