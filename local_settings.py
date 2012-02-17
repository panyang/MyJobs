"""
local_settings.py -- local settings for my.jobs
"""
import os
import sys

import django.views.debug

def wing_debug_hook(*args, **kwargs):
    if __debug__ and 'WINGDB_ACTIVE' in os.environ:
        exc_type, exc_value, traceback = sys.exc_info()
        sys.excepthook(exc_type, exc_value, traceback)
    return old_technical_500_response(*args, **kwargs)

old_technical_500_response = django.views.debug.technical_500_response
django.views.debug.technical_500_response = wing_debug_hook

_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

MEDIA_ROOT = os.path.join(_PATH, 'files', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(_PATH, 'files', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(_PATH, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'


DATABASES = {
    'default': {
        'NAME': 'myjobs',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'alv114',
        'HOST': '',
        'PORT': '3306'
    },
}

ADMINS = (
    ('Mike Seidle', 'mike@directemployers.org'),
)
MANAGERS = ADMINS

# email settings
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'my.jobs'
EMAIL_HOST_PASSWORD = 'ZZ3b7G8f'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'accounts@my.jobs'

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

# Social Auth Settings
TWITTER_CONSUMER_KEY              = 'nRdAOnKMjtl7uqQH5uCVOw'
TWITTER_CONSUMER_SECRET           = 'VwmMl8cefOG8sihA63H36a6911vuAT8doNHsBIj2S4'
FACEBOOK_APP_ID                   = '254116921301793'
FACEBOOK_EXTENDED_PERMISSIONS     = ['offline_access', 'publish_actions']
FACEBOOK_API_SECRET               = 'f30bfa0e87721bbbfbcbad450d68a511'
LINKEDIN_CONSUMER_KEY             = 'x22gjjmqjyu2'
LINKEDIN_CONSUMER_SECRET          = 'pUzRvWhOPZIlmgyG'
ORKUT_CONSUMER_KEY                = ''
ORKUT_CONSUMER_SECRET             = ''
#GOOGLE_OAUTH2_CLIENT_ID           = '957794491021.apps.googleusercontent.com'
#GOOGLE_OAUTH2_CLIENT_SECRET       = '-neb_EKn-shVjnx4JIgPt0g_'
GOOGLE_OAUTH2_CLIENT_ID           = '1016296988275.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'Rf9uLdWPn72mJiFOnO9ONf1F'
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = True
SOCIAL_AUTH_DEFAULT_USERNAME      = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
LOGIN_ERROR_URL                   = '/login/error/'
#SOCIAL_AUTH_USER_MODEL            = 'app.CustomUser'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
GITHUB_APP_ID                     = '3a756c1d5f571118c91f'
GITHUB_API_SECRET                 = '91c51058ae87611e9966762cb8f7dbcc7aed8e7d'
FOURSQUARE_CONSUMER_KEY           = ''
FOURSQUARE_CONSUMER_SECRET        = ''

# Django Social Share Settings
SHARE_NETWORKS = ['facebook', 'linkedin', 'twitter']
SHARE_DEFAULT_URL = u'http://my.jobs'
SHARE_DEFAULT_TITLE = 'Job search power tools.'
SHARE_DEFAULT_DESCRIPTION = 'The right job can change your life.'
SHARE_DEFAULT_URL = u'http://my.jobs'
SHARE_DEFAULT_URL_TITLE = u'My.Jobs puts you in charge of your job search'
SHARE_DEFAULT_URL_DESCRIPTION = 'My.Jobs puts you in charge of your job search.'
SHARE_DEFAULT_IMAGE_URL = u'http://my.jobs/static/myjobslogo.png'
SHARE_DEFAULT_IMAGE_URL_TITLE = 'The title you want automatically inserted in shares'
SHARE_DEFAULT_IMAGE_URL_DESCRIPTION = 'Text you want automatically in description'
SHARE_NETWORKS = [('facebook','Facebook'),('linkedin','LinkedIn'), ('twitter','Twitter'),]
# SHARE_DEFAULT_MESSAGE = 'Default message text'
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
            'filename': "/home/indymike/projects/myjobs/logfile",
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

