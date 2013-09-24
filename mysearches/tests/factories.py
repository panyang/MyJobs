import factory
from myjobs.tests.factories import UserFactory
from mysearches.models import *


class SavedSearchFactory(factory.Factory):
    FACTORY_FOR = SavedSearch
    user = factory.SubFactory(UserFactory)

    url = "http://www.my.jobs/jobs"
    label = "All Jobs"
    feed = "http://www.my.jobs/jobs/feed/rss?"
    is_active = True
    email = "alice@example.com"
    frequency = "W"
    day_of_week = "1"
    notes = "All jobs from www.my.jobs"
    sort_by = "Relevance"


class SavedSearchDigestFactory(factory.Factory):
    FACTORY_FOR = SavedSearchDigest
    user = factory.SubFactory(UserFactory)
    email = "alice@example.com"
    is_active = "True"
