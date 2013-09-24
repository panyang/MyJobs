from secrets import PROD_DB_PASSWD
from default_settings import *

DEBUG = False

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

ALLOWED_HOSTS = ['secure.my.jobs', 'my.jobs', 'localhost']

# Add newrelic here since it shouldn't be used on non-production servers
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('middleware.NewRelic',)
NEW_RELIC_TRACKING = True

# Ensure that https requests to Nginx are treated as secure when forwarded
# to MyJobs
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Browsers should only send the user's session cookie over https
SESSION_COOKIE_SECURE = True