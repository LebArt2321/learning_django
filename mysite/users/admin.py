from django.contrib import admin
from .models import Profile
from .models import CustomUser
from .models import Event


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Event)


