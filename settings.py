"""
settings.py -- Default Django Settings for My.Jobs
"""
from default_settings import *
from secrets import PROD_DB_PASSWD

DEBUG = True

DATABASES = {
    'default':
    {'NAME': 'directseo',
     'ENGINE': 'django.db.backends.sqlite3',
     'USER': '','PASSWORD': '',
     'HOST': '',
     'PORT': '',}
}

# DATABASES = {
#     'default': {
#         'NAME': 'myjobs1',
#         'ENGINE': 'django.db.backends.mysql',
#         'USER': 'db_mjuser',
#         'PASSWORD': PROD_DB_PASSWD,
#         'HOST': 'myjobs.c9shuxvtcmer.us-east-1.rds.amazonaws.com',
#         'PORT': '3306'
#     },
# }

#DATABASES = {
#    'default': {
#        'NAME': 'myjobs',
#        'ENGINE': 'django.db.backends.mysql',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '3306'
#    },
#}

