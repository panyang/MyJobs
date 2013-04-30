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
        try:
            kwargs = {'email': bundle.data.get('email'),
                      'password1': bundle.data.get('password')}
            User.objects.create_inactive_user(**kwargs)
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle
