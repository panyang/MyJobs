from django.shortcuts import render_to_response
from django.template import RequestContext


def test_view(request):
    return render_to_response('myanalytics/tests/test_home.html',
                              context_instance=RequestContext(request))
