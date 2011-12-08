from os.path import abspath, dirname, basename, join
import logging

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)

ADMINS = (
    ('Mike Seidle', 'mike@directemployers.org'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': 'example',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'alv114',
        'HOST': '',
        'PORT': '3306'
    },
}

# email settings
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'my.jobs'
#EMAIL_HOST_USER = 'directemployers'
EMAIL_HOST_PASSWORD = 'ZZ3b7G8f'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'accounts@my.jobs'


TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
ADMIN_MEDIA_PREFIX = '/admin-media/'
MEDIA_URL = ''

SECRET_KEY = 't2eo^kd%k+-##ml3@_x__$j0(ps4p0q6eg*c4ttp9d2n(t!iol'

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'my.urls'

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
    'social_auth',
    'registration',
    'shorty',
    'app',
    'debug_toolbar',
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

# Registration
ACCOUNT_ACTIVATION_DAYS = 14  

# Social Auth
SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook', 'twitter', 'linkedin', 'google-oauth2', 'yahoo')

LOGIN_REDIRECT_URL = '/done'
LOGOUT_REDIRECT_URL = '/accounts/login'

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
            'filename': "/home/web/my/logfile",
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


# Support for loading local settings for development

try:
    from local_settings import *
except:
    pass
