from django.contrib import admin
from .models import Profile
from .models import CustomUser


admin.site.register(CustomUser)
admin.site.register(Profile)

