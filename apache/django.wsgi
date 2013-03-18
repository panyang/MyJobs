import os, sys

import newrelic.agent
newrelic.agent.initialize('/home/web/MyJobs/MyJobs/newrelic.ini')

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
PROJECT_DIR_PARENT = os.path.join(PROJECT_DIR, "../")
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)
if PROJECT_DIR_PARENT not in sys.path:
    sys.path.append(PROJECT_DIR_PARENT)

os.environ['CELERY_LOADER'] = 'django'
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyJobs.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
application = newrelic.agent.wsgi_application()(application)
