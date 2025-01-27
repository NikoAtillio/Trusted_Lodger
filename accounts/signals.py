from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, User, RoomImage
from django.db import models
from PIL import Image

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new User is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(models.signals.post_delete, sender=RoomImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete image file when RoomImage instance is deleted"""
    if instance.image:
        try:
            instance.image.delete(save=False)
        except:
            pass
        
@receiver(post_save, sender=RoomImage)
def resize_image(sender, instance, **kwargs):
    image = Image.open(instance.image.path)
    max_size = (800, 800)
    image.thumbnail(max_size)
    image.save(instance.image.path)