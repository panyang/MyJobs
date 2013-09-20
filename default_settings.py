import djcelery
import logging
import os
import sys

from celery.schedules import crontab
from os.path import abspath, dirname, basename, join
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

from secrets import *

djcelery.setup_loader()

_PATH = os.path.abspath(os.path.dirname(__file__))

APP = abspath(dirname(__file__))
PROJ_ROOT = abspath(dirname(__file__))
sys.path.append(APP)

SECRET_KEY = SECRET_KEY

#TEMPLATE_DEBUG = DEBUG
TEMPLATE_DEBUG = True

# NOTE: ADMINS and MANAGERS in local_settings.py or deploy_settings.py
# NOTE: Databse in local_settings.py or deploy_settings.py

ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = "myjobs"
PROJECT_NAME = basename(ROOT_PATH)

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
# Support for Django Sites framework
SITE_ID = 1
USE_TZ = True
DATE_FORMAT = 'd-M-Y'
# Not a default Django setting, but form formatting differs from model
# formatting. Both are included for potential future l10n changes
# d-M-Y (model) == %d-%b-%Y (form)
FORM_DATE_FORMAT = '%d-%b-%Y'

# Dates of the format "25-Jun-2013" are not in the default list of allowed
# formats.
DATE_INPUT_FORMATS = (
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y',
    '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y',
    '%d %B, %Y',
)

DATE_INPUT_FORMATS += (FORM_DATE_FORMAT,)

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(_PATH, 'files', 'media')
MEDIA_URL = '//d2e48ltfsb5exy.cloudfront.net/myjobs/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJ_ROOT, 'static'),
)

STATIC_ROOT = os.path.join(_PATH, 'files', 'static')
STATIC_URL = '/files/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMIN_MEDIA_PREFIX = '//d2e48ltfsb5exy.cloudfront.net/myjobs/admin/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware', # http auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'middleware.RedirectMiddleware',
    'middleware.XsSharing',
    'django.middleware.locale.LocaleMiddleware',
    )

AUTHENTICATION_BACKENDS = (
    'backends.CaseInsensitiveAuthBackend',
    'django.contrib.auth.backends.ModelBackend', # default
    'django.contrib.auth.backends.RemoteUserBackend', # http
)

ROOT_URLCONF = 'MyJobs.urls'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates')
)


CELERY_IMPORTS = ('MyJobs.tasks',)
CELERY_TIMEZONE = 'US/Eastern'
CELERYBEAT_PIDFILE = '/var/run/celerybeat.pid'
CELERYBEAT_SCHEDULE = {
    'daily-search-digest': {
        'task': 'tasks.send_search_digests',
        'schedule': crontab(minute=0,hour=16),
    },
    'daily-delete-activation': {
        'task': 'tasks.delete_inactive_activations',
        'schedule': crontab(minute=0, hour=2)
    },
    'daily-batch-processing': {
        'task': 'tasks.process_batch_events',
        'schedule': crontab(minute=0, hour=0),
    },
}


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'myjobs.context_processors.current_site_info',
)

INTERNAL_IPS = ('127.0.0.1', '216.136.63.6',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'djcelery',
    'django_jenkins',
    'widget_tweaks',
    'south',
    'django_nose',
    'django_messages',
    'tastypie',
    'captcha',
    'endless_pagination'
)

# Add all MyJobs apps here. This separation ensures that automated Jenkins tests
# only run on these apps
PROJECT_APPS = ('myjobs','myprofile','mysearches','registration',
                'mydashboard', 'mysignon', 'myanalytics')

INSTALLED_APPS += PROJECT_APPS

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pyflakes',
)

# Registration
ACCOUNT_ACTIVATION_DAYS = 14  

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/home'

AUTH_USER_MODEL = 'myjobs.User'

SESSION_SAVE_EVERY_REQUEST = True

MANAGERS = ADMINS

# Logging Settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/home/web/myjobslogs/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console', 'logfile'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'myjobs': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'formatter': 'standard',
        },
        'tasks': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'formatter': 'standard',
        },
    }
}

GRAVATAR_URL_PREFIX = "https://secure.gravatar.com/avatar/"
GRAVATAR_URL_DEFAULT = 404

CAPTCHA_AJAX = True

NEW_RELIC_TRACKING = False

# Modules considered when calculating profile completion
PROFILE_COMPLETION_MODULES = (
    'address',
    'telephone',
    'education',
    'secondaryemail',
    'name', 
    'employmenthistory'
)
