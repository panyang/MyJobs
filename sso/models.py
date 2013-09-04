from hashlib import sha1
import hmac

from django.db import models

from myjobs.models import User


class AuthorizedClient(models.Model):
    user = models.ForeignKey(User)
    site = models.CharField(max_length=255)

    class Meta:
        unique_together = (('user', 'site'),)

    @staticmethod
    def create_key(user):
        return hmac.new(str(user.id),
                        digestmod=sha1).hexdigest()
