from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .models import Favorite, Profile, SellerProfile
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from myapp.models import Product
from .forms import ProfileForm, SellerProfileForm


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = form.cleaned_data['is_seller']
            user.save()
            login(request, user)
            return redirect('myapp:index')
        else:
            print(form.errors)
    form = NewUserForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        favorites = Favorite.objects.filter(user=user)
    except Profile.DoesNotExist:
        # Если профиль не существует, создаем его
        profile = Profile.objects.create(user=user)
        favorites = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'user': user, 'profile': profile, 'favorites': favorites, 'form': form})



@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Перенаправление на страницу профиля после успешного сохранения
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def seller_profile(request, user_id=None):
    user = request.user
    if user_id is None:
        user_id = user.id
    seller = get_object_or_404(CustomUser, id=user_id)
    try:
        seller_profile = SellerProfile.objects.get(user=seller)
    except SellerProfile.DoesNotExist:
        seller_profile = None

    if request.method == "POST":
        if user.id == user_id:
            form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
            if form.is_valid():
                seller_profile = form.save(commit=False)
                seller_profile.user = seller
                seller_profile.save()
                return redirect('users:seller_profile', user_id=user_id)
        else:
            return HttpResponseForbidden()
    else:
        form = SellerProfileForm(instance=seller_profile)

    products = Product.objects.filter(seller=seller)

    background_image = seller_profile.background_image if seller_profile else None
    context = {
        'seller': seller,
        'form': form,
        'seller_profile': seller_profile,
        'products': products,
        'edit_button': user.id == user_id,
        'background_image': background_image,
    }

    return render(request, 'users/sellerprofile.html', context)



@login_required
def edit_seller_profile(request, user_id=None):
    user = request.user
    try:
        seller_profile = SellerProfile.objects.get(user=user)
    except SellerProfile.DoesNotExist:
        seller_profile = None

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
        if form.is_valid():
            seller_profile = form.save(commit=False)
            seller_profile.user = user
            seller_profile.save()
            return redirect('users:sellerprofile', user_id=request.user.id)
    else:
        form = SellerProfileForm(instance=seller_profile)

    context = {
        'form': form,
        'seller_profile': seller_profile,
    }

    return render(request, 'users/edit_seller_profile.html', context)

