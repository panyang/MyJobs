from django.contrib.auth.models import Group
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
    admins = models.ManyToManyField(User, through='CompanyUser')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'

class DashboardModule(models.Model):
    company = models.ForeignKey(Company)

class Microsite(models.Model):
    url = models.URLField(max_length=300)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return 'Microsite %s for %s' % (self.url, self.company.name)

class CompanyUser(models.Model):
    GROUP = Group.objects.get(name='Employer')

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
        self.user.groups.add(self.GROUP)

        super(CompanyUser,self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'company')

def remove_from_staff_group(sender, **kwargs):
    """
    When a CompanyUser instance is deleted, remove the user from the Employer
    group if that user is not also a company user for a different company

    Inputs:
    :sender: Model that sent this signal
    :instance: instance of :sender:
    """
    instance = kwargs.get('instance')
    if CompanyUser.objects.filter(user=instance.user).count() == 1:
        # If the last CompanyUser instance is being deleted for a particular
        # user, also remove that user from the Employer group
        instance.user.groups.remove(instance.GROUP)

# Calls `remove_from_staff_group` after a CompanyUser instance is deleted.
# dispatch_uid: unique string that prevents the signal from being connected
# to multiple times
models.signals.pre_delete.connect(remove_from_staff_group,
                                  sender=CompanyUser,
                                  dispatch_uid='remove_from_staff_group')
