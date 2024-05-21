from django.urls import path
from .views import add_item, update_item, delete_item, add_event, ProductListView, ProductDetailView, add_to_cart, cart_view, remove_from_cart, remove_single_from_cart, autocomplete_search

# from .views import index, indexItem.

app_name = "myapp"

urlpatterns = [
    # path('', index, name='index'),
    path('', ProductListView.as_view(), name='index'),
    # path('<int:my_id>/', indexItem, name="detail"),  
    path('<int:pk>/', ProductDetailView.as_view(), name="detail"), 
    path('autocomplete/', autocomplete_search, name='autocomplete'),
    path('additem/', add_item, name="add_item"), 
    path('addevent/', add_event, name="add_event"), 
    path('updateitem/<int:my_id>/', update_item, name="update_item"), 
    path('deleteitem/<int:my_id>/', delete_item, name="delete_item"), 
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_from_cart/<int:cart_item_id>/', remove_single_from_cart, name='remove_single_from_cart'),
]