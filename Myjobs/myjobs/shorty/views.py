from django.contrib.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from shorty.models import Shorty, Click

class MyShortyList(ListView):
    """implements end user view of shorty history"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args.**kwargs)
    
class MyShortyDetail(DetailView):
    """implements end user detail view of shorty"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args.**kwargs)

class EditShortyDetail(

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args.**kwargs)
