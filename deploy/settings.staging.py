from secrets import PROD_DB_PASSWD
from default_settings import *

DEBUG = True

DATABASES = {
    'default': {
        'NAME': 'myjobs1',
        'ENGINE': 'django.db.backends.mysql',
        #'USER': 'db_mjuser',
        'USER': 'def_mj_root',
        'PASSWORD': PROD_DB_PASSWD,
        #'HOST': 'myjobs.c9shuxvtcmer.us-east-1.rds.amazonaws.com',
        'HOST': 'db-myjobs1.c9shuxvtcmer.us-east-1.rds.amazonaws.com',
        'PORT': '3306'
    },
}

ALLOWED_HOSTS = ['my.jobs', 'localhost']
