import logging
import os
import sys

from os.path import abspath, dirname, basename, join

from secrets import *

#APP = "%s/app" % abspath(dirname(__file__))
#PROJ_ROOT = abspath(dirname(__file__))
#sys.path.append(APP)
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
#PROJECT_NAME = "app"
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

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
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
#    'myurls.middleware.MyUrlsFallbackMiddleware',
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
#    'social_auth',
#    'myurls',
#    'myshare', 
    'app',
    'registration'
)

# AUTHENTICATION_BACKENDS = (
#     'social_auth.backends.twitter.TwitterBackend',
#     'social_auth.backends.facebook.FacebookBackend',
#     'social_auth.backends.google.GoogleOAuth2Backend',
#     'social_auth.backends.yahoo.YahooBackend',
#     'social_auth.backends.contrib.linkedin.LinkedinBackend',
#     'social_auth.backends.OpenIDBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'app.context_processors.current_site_info',
#    'social_auth.context_processors.social_auth_by_type_backends',
)

INTERNAL_IPS = ('127.0.0.1', '216.136.63.6',)

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',   # select one django or
    #'django_jenkins.tasks.dir_tests'      # directory tests discovery
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

# App Specific Settings

# Django Auth
AUTH_PROFILE_MODULE ="app.UserProfile"

# Registration
ACCOUNT_ACTIVATION_DAYS = 14  

# Social Auth
# SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook', 'twitter', 'linkedin', 
#                                 'google-oauth2', 'yahoo')

LOGIN_REDIRECT_URL = '/profile'
LOGOUT_REDIRECT_URL = '/home'

AUTH_USER_MODEL = 'app.User'

MANAGERS = ADMINS

# MyURLS Settings
# MyUrl Specific Settings
# Standard alphabet (a few billion more URLS)
#MYURLS_CHARACTER_SET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
# No vowel character set (a few less billion URLS, butprevents bad words in URLS)
MYURLS_CHARACTER_SET = "0123456789bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
MYURLS_DEFAULT_REDIRECT_TYPE = '302'
MYURLS_DEFAULT_SCHEME = 'http://'
MYURLS_ALLOW_ALL_SITES = True
MYURLS_USE_UTM = True
MYURLS_DEFAULT_VIEW_PREFIX = 'myurl' # default prefix for view based redirector
MYURLS_DEFAULT_UTM_CAMPAIGN = 'myjobs' # campaign name for clicks
MYURLS_DEFAULT_UTM_MEDIUM = 'web' # something like web, email, smoke signals
MYURLS_DEFAULT_UTM_SOURCE = 'my.jobs' # identifies source of traffic
MYURLS_DEFAULT_UTM_CONTENT = 'default' # identifies content for split testing
MYURLS_DEFAULT_APPEND = 'append=true' # Default text to append to URL


# # Django Social Share Settings
# SHARE_NETWORKS = ['facebook', 'linkedin', 'twitter']
# SHARE_DEFAULT_URL = u'http://my.jobs'
# SHARE_DEFAULT_TITLE = 'Job search power tools.'
# SHARE_DEFAULT_DESCRIPTION = 'The right job can change your life.'
# SHARE_DEFAULT_URL = u'http://my.jobs'
# SHARE_DEFAULT_URL_TITLE = u'My.Jobs puts you in charge of your job search'
# SHARE_DEFAULT_URL_DESCRIPTION = 'My.Jobs puts you in charge of your job search.'
# SHARE_DEFAULT_IMAGE_URL = u'http://my.jobs/static/myjobslogo.png'
# SHARE_DEFAULT_IMAGE_URL_TITLE = 'The title you want automatically inserted in shares'
# SHARE_DEFAULT_IMAGE_URL_DESCRIPTION = 'Text you want automatically in description'
# SHARE_NETWORKS = [('facebook','Facebook'),('linkedin','LinkedIn'), ('twitter','Twitter'),]
# # SHARE_DEFAULT_MESSAGE = 'Default message text'
# SHARE_NOTE=''

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
        'app': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'formatter': 'standard',
        },
    }
}
