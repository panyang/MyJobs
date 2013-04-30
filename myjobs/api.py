from django.core import serializers
from django.db import IntegrityError
from django.conf.urls import url
from django.conf.urls.defaults import patterns, url
from django.contrib.auth import authenticate, login

from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from myjobs.models import User
from registration import signals as custom_signals

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        authentication = ApiKeyAuthentication()
        excludes = ('password',)
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        try:
            kwargs = {'email': bundle.data.get('email'),
                      'password1': bundle.data.get('password')}
            user, created = User.objects.create_inactive_user(**kwargs)

            bundle.obj = user
            bundle.data = {'user_created': created}
            return bundle
        except IntegrityError:
            raise BadRequest('That username already exists')
