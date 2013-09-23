import factory

from mymessages.models import *
from myjobs.tests.factories import UserFactory


class MessageFactory(factory.Factory):
    subject = "subject"
    body = "body"
    sent_at = datetime.datetime.now()
    read = False
    expire_at = sent_at + datetime.timedelta(days=2)
    expired = False
    user = factory.SubFactory(UserFactory)
