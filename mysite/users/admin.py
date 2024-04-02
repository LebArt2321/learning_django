from django.contrib import admin
from .models import Profile
from .models import CustomUser
from .models import Event
from .models import Favorite
from .models import SellerProfile


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Favorite)
admin.site.register(SellerProfile)


