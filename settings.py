"""
settings.py -- Default Django Settings for My.Jobs
"""

from os.path import abspath, dirname, basename, join
import logging
import sys

#APP = abspath(dirname(dirname(__file__)))
APP = "%s/app" % abspath(dirname(__file__))
PROJ_ROOT = abspath(dirname(__file__))
sys.path.append(APP)

DEBUG = True
#TEMPLATE_DEBUG = DEBUG
TEMPLATE_DEBUG = True

# NOTE: ADMINS and MANAGERS in local_settings.py or deploy_settings.py
# NOTE: Databse in local_settings.py or deploy_settings.py

ROOT_PATH = abspath(dirname(__file__))
#PROJECT_NAME = "app"
PROJECT_NAME = basename(ROOT_PATH)

<<<<<<< HEAD
=======
ADMINS = (
    ('Mike Seidle', 'mike@directemployers.org'),
)
MANAGERS = ADMINS


>>>>>>> File maintenance

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
# Support for Django Sites framework
SITE_ID = 1

USE_I18N = True
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = abspath(join(PROJ_ROOT, 'media', 'uploads'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = abspath(join(PROJ_ROOT, 'media', 'static'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'


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
    'myurls.middleware.MyUrlsFallbackMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'myjobs.urls'

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
    'social_auth',
    'registration',
    'myurls',
    'myshare', 
    'app',
    #'debug_toolbar',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.OpenIDBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'app.context_processors.current_site_info',
    'social_auth.context_processors.social_auth_by_type_backends',
    #'social_auth.context_processors.social_auth_by_name_backends',
    #'social_auth.context_processors.social_auth_backends',
    #'social_auth.context_processors.backends_data',
)

INTERNAL_IPS = ('127.0.0.1', '216.136.63.6',)

# App Specific Settings

# Django Auth
AUTH_PROFILE_MODULE ="app.UserProfile"

# Registration
ACCOUNT_ACTIVATION_DAYS = 14  

# Social Auth
SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook', 'twitter', 'linkedin', 
                                'google-oauth2', 'yahoo')

LOGIN_REDIRECT_URL = '/profile'
LOGOUT_REDIRECT_URL = '/home'

# Support for loading local settings for development
try:
    from local_settings import *
except ImportError, exp:
    pass
