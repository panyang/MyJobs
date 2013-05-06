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
from tastypie.serializers import Serializer
from tastypie.utils import trailing_slash

from myjobs.models import User
from mysearches.helpers import validate_dotjobs_url
from mysearches.models import SavedSearch
from registration import signals as custom_signals

class UserResource(ModelResource):
    searches = fields.ToManyField('myjobs.api.SavedSearchResource',
                                  'savedsearch_set')

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        authentication = ApiKeyAuthentication()
        excludes = ('password',)
        always_return_data = True
        serializer = Serializer(formats=['jsonp', 'json'],
                                content_types={'jsonp':'text/javascript',
                                               'json':'application/json'})

    def full_dehydrate(self, bundle):
        return bundle

    def obj_create(self, bundle, **kwargs):
        if not bundle.data.get('email'):
            raise BadRequest('No email provided')
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
        serializer = Serializer(formats=['jsonp', 'json'],
                                content_types={'jsonp':'text/javascript',
                                               'json':'application/json'})

    def full_dehydrate(self, bundle):
        return bundle

    def obj_create(self, bundle, **kwargs):
        email = bundle.data.get('email')
        if not email:
            raise BadRequest('No email provided')
        user = User.objects.get_email_owner(email=email)
        if not user:
            raise BadRequest('User owning email %s does not exist' % email)
        try:
            SavedSearch.objects.get(user=user,
                                    url=bundle.data.get('url'))
            raise BadRequest('User %s already has a search for %s' % \
                (user.email, bundle.data.get('url')))
        except SavedSearch.DoesNotExist:
            pass

        frequency = bundle.data.get('frequency')
        day_of_week = bundle.data.get('day_of_week')
        day_of_month = bundle.data.get('day_of_month')
        if not frequency:
            frequency = 'D'
        elif frequency == 'M' and not day_of_month:
            raise BadRequest('Must supply day_of_month')
        elif frequency == 'W' and not day_of_week:
            raise BadRequest('Must supply day_of_week')

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
                       'user': user,
                       'email': email,
                       'frequency': frequency,
                       'day_of_week': day_of_week,
                       'day_of_month': day_of_month,
                       'notes': notes}
        search = SavedSearch.objects.create(**search_args)
        bundle.obj = search
        bundle.data = {'email': bundle.data.get('email'),
                       'frequency': bundle.data.get('frequency', 'D'),
                       'new_search': True}
        return bundle
