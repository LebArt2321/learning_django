from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='_profile_images')
    contact_number = models.CharField(max_length=30, default='+79123213212')

    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images')
    date = models.DateField()
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')

    def __str__(self):
        return self.name
