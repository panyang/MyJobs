from django.db import IntegrityError
from django.conf.urls import url
from django.conf.urls.defaults import patterns, url
from django.contrib.auth import authenticate, login

from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from myjobs.models import User
from registration import signals as custom_signals

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        """
        Custom create sets password, active state, and gravatar on post
        """

        try:
            bundle = self.full_hydrate(bundle)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.is_active = False
            bundle.obj.gravatar = bundle.data.get('email')
            bundle.obj.save()

            custom_signals.email_created.send(sender=self,user=bundle.obj,
                                              email=bundle.obj.email )
            custom_signals.send_activation.send(sender=self,user=bundle.obj,
                                                email=bundle.obj.email)
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle
