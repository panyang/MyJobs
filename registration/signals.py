from registration import models 
from django.dispatch import Signal, receiver

email_created = Signal(providing_args=["user","email"])

@receiver(email_created)
def create_activation_profile(sender,**kwargs):
    """
    Signalled when any email is created (whether as the primary user email or
    a secondary email)
    """
    
    user = kwargs.get("user")
    email = kwargs.get("email")
    activation = models.ActivationProfile.objects.create(user=user,email=email)

send_activation = Signal(providing_args=["user","email"])

@receiver(send_activation)
def send_activation_email(sender,**kwargs):
    """
    Triggers an email that has the activation link  automatically when a user
    creates an account but triggered manually for secondard email creation.
    """
    
    user = kwargs.get("user")
    email = kwargs.get("email")
    activation = models.ActivationProfile.objects.get(user=user,email=email)
    activation.send_activation_email()

