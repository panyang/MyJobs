from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

from myjobs.decorators import user_is_allowed
from myjobs.models import User
from mymessages.models import Message


@user_is_allowed()
@user_passes_test(User.objects.not_disabled)
def read(request):
    if request.POST:
        message, user = request.POST.get('name').split('-')[1:]
        m = Message.objects.get(id=message)
        m.mark_read()
        return HttpResponse('')
