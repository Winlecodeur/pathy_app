from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notif, Post

@receiver(post_save, sender=Post)
def created_notif(sender, instance, created, **kwargs):
    if created : 
        users = User.objects.all()
        for user in users : 
            Notif.objects.created(user=user, post=instance)