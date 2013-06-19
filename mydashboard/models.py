from django.db import models

from myjobs.models import *
from myprofile.models import *


class Company(models.Model):
    """
    Companies are the central hub for a group of modules and admins (Users).

    """
    # Why isn't the primary key an auto incrementing field?
    # To keep the my.jobs Company model in sync with the microsites Company
    # model the id is the same to ease the transition to a single model down the
    # line.
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    admins = models.ManyToManyField(User, through='Administrators')

class DashboardModule(models.Model):
    company = models.ForeignKey(Company)

class Administrators(models.Model):
    admin = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    date_added = models.DateTimeField(auto_now=True)
