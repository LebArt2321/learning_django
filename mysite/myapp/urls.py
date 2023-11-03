from django.urls import path
from .views import index, indexItem, add_item

app_name = "myapp"

urlpatterns = [
    path('', index),
    path('<int:my_id>/', indexItem, name="detail"),  
    path('additem/', add_item, name="add_item"), 
]