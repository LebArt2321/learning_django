# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, SizeViewSet, ProductSizeViewSet
from .views import CustomUserViewSet, ProfileViewSet, SellerProfileViewSet, EventViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'productSize', ProductSizeViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'seller-profiles', SellerProfileViewSet)
router.register(r'events', EventViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
