import factory
import datetime
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


class EducationFactory(factory.Factory):
    FACTORY_FOR = Education

    organization_name = "College"
    degree_date = datetime.date(2005, 1, 2)
    city_name = "Indianapolis"
    country_code = "IN"
    education_level_code = 6
    education_score = "4.0"
    degree_name = "Art"
    degree_major = "Worksmanship"
    degree_minor = "English"
    user = factory.SubFactory(UserFactory)


class AddressFactory(factory.Factory):
    FACTORY_FOR = Address

    label = "Home"
    address_line_one = "1234 Thing Road"
    address_line_two = "Apt. 8"
    city_name = "Indianapolis"
    country_code = "IN"
    postal_code = "12345"
    user = factory.SubFactory(UserFactory)


class TelephoneFactory(factory.Factory):
    FACTORY_FOR = Telephone

    use_code = "Home"
    area_dialing = "(123)"
    number = "456-7890"
    user = factory.SubFactory(UserFactory)


class EmploymentHistoryFactory(factory.Factory):
    FACTORY_FOR = EmploymentHistory

    position_title = "Handler"
    organization_name = "Mr. Wrench"
    start_date = datetime.date(2005, 3, 4)
    current_indicator = True
    user = factory.SubFactory(UserFactory)
