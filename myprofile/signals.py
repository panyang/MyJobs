from myprofile import models
from django.dispatch import Signal, receiver

activated = Signal(providing_args=["user","email"])
@receiver(activated)
def activate_email(sender,**kwargs):
    user = kwargs.get("user")
    email = kwargs.get("email")

    if user.email == email:
        user.is_active = True
        user.save()
    else:
        email = models.SecondaryEmail.objects.get(user=user,email=email)
        email.verified = True
        email.save()
