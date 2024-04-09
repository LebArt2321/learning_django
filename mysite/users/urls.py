from django.urls import path
from .views import register, profile, seller_profile, edit_seller_profile, edit_profile
from django.contrib.auth.views import LoginView, LogoutView


app_name = "users"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Перенаправление на главную страницу
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('sellerprofile/<int:user_id>/', seller_profile, name='sellerprofile'),
    path('edit_seller_profile/<int:user_id>/', edit_seller_profile, name='edit_seller_profile'),
]