from datetime import datetime
import json
from urlparse import urlparse

from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from myanalytics.models import SiteViewer, SiteView, UserAgent


@csrf_exempt
def track(request):
    rand = request.REQUEST.get('r')
    # Ensure that the request is not tracked multiple times
    if not cache.get(rand):
        aguid = request.REQUEST.get('_id')
        user = None if request.user.is_anonymous() else request.user

        viewer = SiteViewer.objects.get_or_create(aguid=aguid,
                                                  user=user)[0]
        viewer.view_count = viewer.view_count + 1
        viewer.save()

        ua = request.REQUEST.get('ua')
        user_agent = UserAgent.objects.get_or_create(user_agent=ua)[0]

        ip = request.META['REMOTE_ADDR']
        view_time = float(request.REQUEST.get('_viewts'))
        view_time = datetime.fromtimestamp(view_time)
        resolution_w = request.REQUEST.get('res_w')
        resolution_h = request.REQUEST.get('res_h')
        url = request.REQUEST.get('url')
        search = unicode(urlparse(url).query)

        view_data = {'ip': ip, 'viewed': view_time, 'site_url': url,
                     'search_parameters': search, 'resolution_w': resolution_w,
                     'resolution_h': resolution_h, 'viewer': viewer,
                     'user_agent': user_agent}

        goal = request.REQUEST.get('idgoal')
        if goal:
            view_data['goal'] = goal
            if goal == 'apply':
                try:
                    apply_url = json.loads(request.REQUEST.get(
                        '_cvar'))['1'][1]
                except (KeyError, TypeError):
                    # KeyError: cvar at index '1' was not provided
                    # TypeError: json.loads received bad data; cvar was
                    #   not provided?
                    apply_url = 'error'
                view_data['goal_url'] = apply_url
            elif goal == 'save search':
                # What do we want to do with this information?
                pass
            elif goal == 'share':
                try:
                    share_site = json.loads(request.REQUEST.get(
                        '_cvar'))['1'][1]
                except (KeyError, TypeError):
                    # KeyError: cvar at index '1' was not provided
                    # TypeError: json.loads received bad data; cvar was
                    #   not provided?
                    share_site = 'error'
                view_data['share_site'] = share_site

        site_view = SiteView.objects.create(**view_data)

    cache.set(rand, rand, 10)

    pixel = 'R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==\n'
    return HttpResponse(pixel.decode('base64'), content_type='image/gif')
