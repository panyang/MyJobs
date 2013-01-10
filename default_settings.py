import logging
import os
import sys

from os.path import abspath, dirname, basename, join

from secrets import *

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

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(_PATH, 'files', 'media')
MEDIA_URL = 'http://src.nlx.org/myjobs/admin/'

STATIC_ROOT = os.path.join(_PATH, 'files', 'static')
STATIC_URL = '/files/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMIN_MEDIA_PREFIX = 'http://src.nlx.org/myjobs/admin/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'MyJobs.urls'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates')
)

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
    'django_jenkins',
    'widget_tweaks',
    'myjobs',
    'myprofile',
    'registration',
    'south'
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'myjobs.context_processors.current_site_info',
)

INTERNAL_IPS = ('127.0.0.1', '216.136.63.6',)

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)


# Registration
ACCOUNT_ACTIVATION_DAYS = 14  

LOGIN_REDIRECT_URL = '/account'
LOGOUT_REDIRECT_URL = '/home'

AUTH_USER_MODEL = 'myjobs.User'

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
    }
}
