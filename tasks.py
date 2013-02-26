from celery import task
from celery.schedules import crontab

from itertools import chain 
from mysearches.models import SavedSearch, SavedSearchDigest
from datetime import datetime

@task(name='tasks.send_search_digests')
def send_search_digests():
    today = datetime.today()
    day_of_week = today.isoweekday()

    digest = SavedSearchDigest.objects.filter(default=True)
    digest.send_email()
    
    not_digest = SavedSearchDigest.objects.filter(default=False)    
    for item in not_digest:
        saved_searches = item.user.savedsearch_set.all()
        daily = saved_searches.objects.filter(frequency='D')
        weekly = saved_searches.objects.filter(day_of_week=str(day_of_week))
        monthly = saved_searches.objects.filter(day_of_month=today.day)

        saved_search_objs = chain(daily, weekly, monthly)
        for search_obj in saved_search_objs:
            search_obj.send_email()
            search_obj.last_sent = datetime.now()
            search_obj.save()
