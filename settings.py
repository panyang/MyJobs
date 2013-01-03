from default_settings import *
try: #pull in local settings, if it exists. Primarily only for development.
    from local_settings import *
except:
    pass
    
from secrets import PROD_DB_PASSWD
 
DEBUG = True
 
DATABASES = {
    'default': {
        'NAME': 'myjobs1',
        'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'db_mjuser',
        'PASSWORD': PROD_DB_PASSWD,
        'HOST': 'myjobs.c9shuxvtcmer.us-east-1.rds.amazonaws.com',
        'PORT': '3306'
    },
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'myjobs'
#    },
#}

