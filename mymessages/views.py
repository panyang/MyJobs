from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext, loader

@login_required
def messages(request):
	"""
	The inbox for a given user.

	"""

	import ipdb
	ipdb.set_trace()

	data_dict = {}
	return render_to_response("myjobs_base.html", data_dict, 
							  context_instance=RequestContext(request))


@login_required
def new_message(request):
	pass


@login_required
def read_message(request):
	pass


@login_required
def delete_message(request):
	pass
