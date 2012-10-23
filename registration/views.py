from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def login_user(request):
    username=''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/profile')
    return render_to_response('registration/login.html', {'username': username},
    context_instance=RequestContext(request))
