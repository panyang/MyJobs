from myprofile import models
from django.dispatch import Signal, receiver

activated = Signal(providing_args=["user","email"])
@receiver(activated)
def activate_email(sender,**kwargs):
    """
    Signalled when an activation profile is activated and the corresponding
    changes need to be made to the User or SecondaryEmail object.
    """
    
    user = kwargs.get("user")
    email = kwargs.get("email")

    if user.email == email:
        user.is_active = True
        user.is_disabled = False
        user.save()
    else:
        email = models.SecondaryEmail.objects.get(user=user,
                                                  email__iexact=email)
        email.verified = True
        email.save()
