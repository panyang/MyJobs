import datetime

from django.core import serializers
from django.db import IntegrityError
from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, login

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.utils import trailing_slash
from tastypie.validation import Validation

from myjobs.models import User
from mysearches.forms import SavedSearchForm
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
            error = {'email': 'No email provided'}
            raise ImmediateHttpResponse(self.error_response(
                                            bundle.request,
                                            error,
                                            response_class=HttpBadRequest))
        try:
            kwargs = {'email': bundle.data.get('email'),
                      'password1': bundle.data.get('password')}
            user, created = User.objects.create_inactive_user(**kwargs)

            bundle.obj = user
            bundle.data = {'user_created': created}
            return bundle
        except IntegrityError:
            error = {'email': 'That username already exists'}
            raise ImmediateHttpResponse(self.error_response(
                                            bundle.request,
                                            error,
                                            response_class=HttpBadRequest))


class CustomSearchValidation(Validation):
    def is_valid(self, bundle, request):
        if not bundle.data:
            return {'__all__':'No information provided'}

        errors = {}

        email = bundle.data.get('email', '')
        if not email:
            errors['email'] = 'No email provided'
        else:
            user = User.objects.get_email_owner(email=email)
            if not user:
                errors['email'] = 'No user with email %s exists' % email

        url = bundle.data.get('url', '')
        if not url:
            errors['url'] = 'No .JOBS feed provided'
        else:
            try:
                user = User.objects.get_email_owner(email=email)
                if user:
                    SavedSearch.objects.get(user=user,
                                            url=bundle.data.get('url'))
                    errors['url'] = 'User %s already has a search for %s' % \
                                    (email, url)
            except SavedSearch.DoesNotExist:
                label, feed = validate_dotjobs_url(url)
                if not (label and feed):
                    errors['url'] = 'This is not a valid .JOBS feed'
                else:
                    bundle.data['label'] = label
                    bundle.data['feed'] = feed

        frequency = bundle.data.get('frequency')
        day_of_month = bundle.data.get('day_of_month')
        day_of_week = bundle.data.get('day_of_week')
        if not frequency:
            bundle.data['frequency'] = 'D'
        elif frequency == 'W':
            if not day_of_week:
                errors['day_of_week'] = 'Must supply day_of_week'
            elif day_of_week not in map(str, range(1,8)):
                errors['day_of_week'] = 'day_of_week %s outside range ' \
                                        '"1".."7"' % day_of_week
        elif frequency == 'M':
            if not day_of_month:
                errors['day_of_month'] = 'Must supply day_of_month'
            elif day_of_month not in range(1,31):
                errors['day_of_month'] = 'day_of_month %s outside range ' \
                                        '1..30' % day_of_month
        return errors

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
        validation = CustomSearchValidation()

    def full_dehydrate(self, bundle):
        return bundle

    def obj_create(self, bundle, **kwargs):
        self.is_valid(bundle)
        if bundle.errors:
            raise ImmediateHttpResponse(self.error_response(
                                            bundle.request,
                                            bundle.errors['savedsearch'],
                                            response_class=HttpBadRequest))
        user = User.objects.get_email_owner(bundle.data.get('email'))
        notes = bundle.data.get('notes', '')
        if not notes:
            # Monday, April 29, 2013 10:26 AM
            now = datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M %p')
            notes += 'Sent on ' + now
            if bundle.request:
                notes += ' from ' + bundle.request.get_host()
            bundle.data['notes'] = notes

        search_args = {'url': bundle.data.get('url'),
                       'label': bundle.data.get('label'),
                       'feed': bundle.data.get('feed'),
                       'user': user,
                       'email': bundle.data.get('email'),
                       'frequency': bundle.data.get('frequency'),
                       'day_of_week': bundle.data.get('day_of_week'),
                       'day_of_month': bundle.data.get('day_of_month'),
                       'notes': notes}
        search = SavedSearch.objects.create(**search_args)
        bundle.obj = search
        bundle.data = {'email': bundle.data.get('email'),
                       'frequency': bundle.data.get('frequency', 'D'),
                       'new_search': True}
        return bundle
