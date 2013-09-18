from django.http import HttpResponse
from pprint import pprint


def track(request):
    pprint(request.GET)
    return HttpResponse(status=200)
