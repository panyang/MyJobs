import factory
from myjobs.models import *

class UserFactory(factory.Factory):
    FACTORY_FOR = User
    email = 'alice@example.com'
    gravatar = 'alice@example.com'
    password = 'secret'
    user_guid = factory.LazyAttribute(lambda n: '{0}'.format(uuid.uuid4()))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
