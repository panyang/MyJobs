import factory

from myjobs.tests.factories import UserFactory
from mysignon.models import AuthorizedClient


class AuthorizedClientFactory(factory.Factory):
    FACTORY_FOR = AuthorizedClient

    user = factory.SubFactory(UserFactory)
    site = 'my.jobs'
