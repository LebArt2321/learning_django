from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from myapp.models import Product, ProductSize

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='_profile_images')
    contact_number = models.CharField(max_length=30, default='+79123213212')
    height = models.IntegerField(blank=True, null=True)
    foot_size = models.IntegerField(blank=True, null=True)
    chest_circumference = models.IntegerField(blank=True, null=True) # обхват груди
    waist_circumference = models.IntegerField(blank=True, null=True) # обхват талии
    hip_girth = models.IntegerField(blank=True, null=True) # обхват бедер
    shoulder_width = models.IntegerField(blank=True, null=True) # ширина плеч
    length_shoulder = models.IntegerField(blank=True, null=True) # длина рукава от плеча
    pants_length = models.IntegerField(blank=True, null=True) # длина штанов

    def __str__(self):
        return self.user.username

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='_profile_images')
    contact_number = models.CharField(max_length=30, default='+79123213212')
    seller_description = models.TextField(blank=True)
    background_image = models.ImageField(blank=True, upload_to='_background_images')

    def __str__(self):
        return f"Seller Profile - {self.user.username}"

class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images')
    date = models.DateField()
    description = models.CharField(max_length=2000, default='')
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s favorite {self.product.name}"

