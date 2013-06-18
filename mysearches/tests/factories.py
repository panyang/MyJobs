import factory
from myjobs.tests.factories import UserFactory
from mysearches.models import *


class SavedSearchFactory(factory.Factory):
    FACTORY_FOR = SavedSearch
    user = factory.SubFactory(UserFactory)

    url = "http://jobs.jobs/jobs"
    label = "All Jobs"
    feed = "http://jobs.jobs/jobs/feed/rss"
    is_active = True
    email = "alice@example.com"
    frequency = "W"
    day_of_week = "1"
    notes = "All jobs from jobs.jobs"


class SavedSearchDigestFactory(factory.Factory):
    FACTORY_FOR = SavedSearchDigest
    user = factory.SubFactory(UserFactory)
    email = "alice@example.com"
    is_active = "True"
