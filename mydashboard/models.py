from django.contrib.auth.models import Group
from django.db import models

from myjobs.models import User


class Company(models.Model):
    """
    Companies are the central hub for a group of modules and employers.

    *** Why isn't the primary key an auto incrementing field? ***
    To keep the my.jobs Company model in sync with the microsites Company
    model the id is the same to ease the transition to a single model down the
    line.

    """
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    admins = models.ManyToManyField(User, through='CompanyUser')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'


class CandidateEvent(models.Model):
    """
    Something happened! This log tracks job views and saved searches.
    
    """
    who = models.ForeignKey(User)
    whom = models.ForeignKey(Company)
    what = models.CharField(max_length=255)
    where = models.URLField(max_length=300)
    when = models.DateTimeField(auto_now=True)


class DashboardModule(models.Model):
    company = models.ForeignKey(Company)

class Microsite(models.Model):
    url = models.URLField(max_length=300)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return 'Microsite %s for %s' % (self.url, self.company.name)

class CompanyUser(models.Model):
    GROUP_NAME = 'Employer'

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Admin %s for %s' % (self.user.email, self.company.name)


    def save(self, *args, **kwargs):
        """
        Adds the user to the Employer group if it wasn't already a member.

        If the user is already a member of the Employer group, the Group app
        is smart enough to not add it a second time.
        """
        group = Group.objects.get(name=self.GROUP_NAME)
        self.user.groups.add(group)

        super(CompanyUser,self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'company')
