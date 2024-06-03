# api/views.py
from rest_framework import viewsets  # Добавьте этот импорт
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ProductSerializer, CategorySerializer, SizeSerializer, ProductSizeSerializer,
    CustomUserSerializer, ProfileSerializer, SellerProfileSerializer, EventSerializer, FavoriteSerializer,
    RegisterSerializer
)
from myapp.models import Product, Category, Size, ProductSize
from users.models import CustomUser, Profile, SellerProfile, Event, Favorite

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class ProductSizeViewSet(viewsets.ModelViewSet):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'sizes': reverse('size-list', request=request, format=format),
        'productSize': reverse('productsize-list', request=request, format=format),
        'users': reverse('customuser-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format),
        'seller-profiles': reverse('sellerprofile-list', request=request, format=format),
        'events': reverse('event-list', request=request, format=format),
        'favorites': reverse('favorite-list', request=request, format=format),
        'register': reverse('register', request=request, format=format),
        'token': reverse('token_obtain_pair', request=request, format=format),
        'token-refresh': reverse('token_refresh', request=request, format=format),
    })
