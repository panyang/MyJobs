from django.db import models
from myjobs.models import User

class Message(models.Model):
   subject = models.CharField(max_length=255, blank=True)
   message_body = models.TextField(blank=True) 
   date_sent = models.DateTimeField(auto_now_add=True, editable=False)
   date_read = models.DateTimeField(null=True, editable=False)
   recipient = models.ForeignKey(User)
   sender = models.CharField(max_length=255, blank=True, editable=False)
   priority = models.IntegerField()
