from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP

@receiver(post_save, sender=RSVP)
def send_rsvp_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event
        send_mail(
            'RSVP Confirmation',
            f'Hello {user.username},\n\nYou have successfully RSVPed for the event: {event.name}.',
            "sumaiyameem.cse6.bu@gmail.com",
            [user.email],
            fail_silently=False,
        )
