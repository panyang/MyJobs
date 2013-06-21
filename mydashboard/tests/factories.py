import factory

from mydashboard.models import *

class CompanyFactory(factory.Factory):
    FACTORY_FOR = Company
    id = 1
    name = 'Test Company'
