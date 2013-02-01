import factory
from myjobs.tests.factories import UserFactory
from myprofile.models import *


class SecondaryEmailFactory(factory.Factory):
    FACTORY_FOR = SecondaryEmail

    user = factory.SubFactory(UserFactory)
    email = "alicia.smith@foo.com"
    label = "Personal"


class PrimaryNameFactory(factory.Factory):
    FACTORY_FOR = Name
    given_name = "Alice"
    family_name = "Smith"
    primary = True
    user = factory.SubFactory(UserFactory)


class NewPrimaryNameFactory(factory.Factory):
    FACTORY_FOR = Name
    given_name = "Alicia"
    family_name = "Smith"
    primary = True
    user = factory.SubFactory(UserFactory)
