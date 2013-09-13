import factory

from myjobs.tests.factories import UserFactory
from mydashboard.models import *


class CompanyFactory(factory.Factory):
    FACTORY_FOR = Company

    id = 1
    name = 'Test Company'


class MicrositeFactory(factory.Factory):
    FACTORY_FOR = Microsite

    url = 'http://test.jobs'
    company = factory.SubFactory(CompanyFactory)


class CompanyUserFactory(factory.Factory):
    FACTORY_FOR = CompanyUser

    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
