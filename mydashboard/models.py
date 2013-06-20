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
    admins = models.ManyToManyField(User, through='Administrators')

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

class Administrators(models.Model):
    STAFF_GROUP = Group.objects.get(name='Staff')

    admin = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Admin %s for %s' % (self.admin.email, self.company.name)

    def clean(self):
        """
        Each user:company mapping is unique; Attempting to add a user as an
        admin for the same company multiple times is bad.
        """
        if Administrators.objects.filter(admin=self.admin,
                                         company=self.company).exists():
            validation_str = 'Admin with email "%s" already exists for %s' % \
                                 (self.admin.email, self.company.name)
            raise ValidationError(validation_str)
        super(Administrators, self).clean()

    def save(self, *args, **kwargs):
        """
        Adds the user to the Staff group if it wasn't already a member.

        If the user is already a member of the Staff group, the Group app
        is smart enough to not add it a second time.
        """
        self.admin.groups.add(self.STAFF_GROUP)

        super(Administrators,self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'administrator'

def remove_from_staff_group(sender, **kwargs):
    """
    When an dministrator instance is deleted, remove the user from the staff
    group if that user is not also an administrator for a different company

    Inputs:
    :sender: Model that sent this signal
    :instance: instance of :sender:
    """
    instance = kwargs.get('instance')
    if Administrators.objects.filter(admin=instance.admin).count() == 1:
        # If the last Administrators instance is being deleted for a particular
        # user, also remove that user from the Staff group
        instance.admin.groups.remove(instance.STAFF_GROUP)

# Calls `remove_from_staff_group` after an Administrator instance is deleted.
# dispatch_uid: unique string that prevents the signal from being connected
# to multiple times
models.signals.pre_delete.connect(remove_from_staff_group,
                                  sender=Administrators,
                                  dispatch_uid='remove_from_staff_group')
