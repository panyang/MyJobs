import datetime

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin import widgets

from mymessages.models import Message
from myjobs.models import User


class AdminMessageForm(forms.ModelForm):
    group = forms.MultipleChoiceField(label=_('Group'), required=True,
                                      help_text=
                                      "Send message to selected group(s).")

    def __init__(self, *args, **kwargs):
        super(AdminMessageForm, self).__init__(*args, **kwargs)
        self.fields['group'].choices = self._get_group_choices()
        self.fields['group'].widget.attrs['size'] = '5'
        self.fields['expire_at'].widget = widgets.AdminSplitDateTime()

    def _get_group_choices(self):
        return [('all', _('All users'))] + \
               [(group.pk, group.name) for group in Group.objects.all()]

    class Meta:
        model = Message


class AdminMessage(admin.ModelAdmin):
    form = AdminMessageForm
    list_display = ('subject', 'user', 'sent_at', 'read', 'read_at', 'expired')
    search_fields = ['user__email']
    fieldsets = (
        ('Send to', {
            'fields': (
                'group',
            ),
        }),
        ('Message', {
            'fields': (
                'subject', 'body'
            ),
        }),
        (None, {
            'fields': (
                'expire_at',
            )
        })
    )

    def save_model(self, request, obj, form, change):
        group = form.cleaned_data['group']
        subject = form.cleaned_data['subject']
        body = form.cleaned_data['body']
        expire = form.cleaned_data['expire_at']
        if group[0] == 'all':
            users = User.objects.all()
        else:
            group = Group.objects.get(pk=int(group[0]))
            users = User.objects.filter(groups=group)

        for user in users:
            if user.is_active:
                obj.pk = None
                obj.user, obj.subject, obj.body, obj.sent_at, obj.expire_at = \
                    user, subject, body, datetime.datetime.now(), expire
                obj.save()

admin.site.register(Message, AdminMessage)