from django import forms
from django.contrib import admin

from mymessages.models import Message, MessageInfo
from myjobs.models import User


class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = Message


class AdminMessage(admin.ModelAdmin):
    form = AdminMessageForm
    list_display = ('subject', 'start_on', 'expire_at')
    fieldsets = (
        ('Send to', {
            'fields': (
                'group',
            ),
        }),
        ('Message', {
            'fields': (
                'message_type', 'subject', 'body', 'btn_text',
            ),
        }),
        (None, {
            'fields': (
                'start_on', 'expire_at',
            )
        })
    )

    def save_model(self, request, obj, form, change):
        """
        Saves Message Object.  For each Message.groups gather the users in
        that group and create a MessageInfo connecting the user to the Message
        if that user currently does not have this Message.
        """
        groups = form.cleaned_data['group']
        obj.save()
        for group in groups:
            users = User.objects.filter(groups=group)
            for user in users:
                try:
                    MessageInfo.objects.get(user=user, message=obj)
                except MessageInfo.DoesNotExist:
                    new = MessageInfo(user=user, message=obj)
                    new.save()
                else:
                    continue


admin.site.register(Message, AdminMessage)
