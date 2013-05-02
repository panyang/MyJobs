import datetime

from django.core import serializers
from django.db import IntegrityError
from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, login

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from myjobs.models import User
from mysearches.helpers import validate_dotjobs_url
from mysearches.models import SavedSearch
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

class SavedSearchResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = SavedSearch.objects.all()
        resource_name = 'savedsearch'
        authorization = Authorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        authentication = ApiKeyAuthentication()
        always_return_data = True

    def full_dehydrate(self, bundle):
        return bundle

    def obj_create(self, bundle, **kwargs):
        ur = UserResource()
        user_bundle = ur.build_bundle()
        user_bundle.data['email'] = bundle.data.get('email')
        user_bundle = ur.obj_create(user_bundle)

        label, feed = validate_dotjobs_url(bundle.data.get('url'))
        if not (label and feed):
            raise BadRequest('This is not a valid .JOBS feed')

        notes = bundle.data.get('notes', '')
        if not notes:
            # Monday, April 29, 2013 10:26 AM
            now = datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M %p')
            notes += 'Sent on ' + now
            if bundle.request:
                notes += ' from ' + bundle.request.get_host()

        search_args = {'url': bundle.data.get('url'),
                       'label': label,
                       'feed': feed,
                       'user': user_bundle.obj,
                       'email': bundle.data.get('email'),
                       'frequency': bundle.data.get('frequency', 'D'),
                       'day_of_week': bundle.data.get('day_of_week'),
                       'day_of_month': bundle.data.get('day_of_month'),
                       'notes': notes}
        search = SavedSearch.objects.create(**search_args)
        bundle.obj = search
        bundle.data = {'email': bundle.data.get('email'),
                       'frequency': bundle.data.get('frequency', 'D'),
                       'new_user': user_bundle.data.get('user_created'),
                       'new_search': True}
        return bundle
