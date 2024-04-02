from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .models import Profile, SellerProfile
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
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
    except Profile.DoesNotExist:
        profile = None
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')  # Redirect to the same page or wherever you want
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)


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


# @login_required
# def profile(request):
#     if request.method == "POST":
#         contact_number = request.POST.get("contact_number")
#         image = request.FILES.get('upload')
#         user = request.user
#         person = Profile(user=user,contact_number=contact_number, image=image)
#         person.save()
#     return render(request, 'users/profile.html')



# def seller_profile(request, id):
#     seller = CustomUser.objects.get(id=id)
#     products = Product.objects.filter(seller=seller)
    
#     context = {
#         'seller': seller,
#         'products': products
#     }
    
#     return render(request, 'users/sellerprofile.html', context)

# @login_required
# def edit_seller_profile(request):
#     user = request.user
#     try:
#         seller_profile = SellerProfile.objects.get(user=user)
#     except SellerProfile.DoesNotExist:
#         seller_profile = None
    
#     if request.method == "POST":
#         form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
#         if form.is_valid():
#             seller_profile = form.save(commit=False)
#             seller_profile.user = user
#             seller_profile.save()
#             return redirect('users/sellerprofile.html', id=user.id)  # Redirect to the same page or wherever you want
#     else:
#         form = SellerProfileForm(instance=seller_profile)
    
#     context = {
#         'form': form,
#         'seller_profile': seller_profile,
#     }
    
#     return render(request, 'users/edit_seller_profile.html', context)

# @login_required
# def seller_profile(request, id):
#     seller = CustomUser.objects.get(id=id)
#     try:
#         seller_profile = SellerProfile.objects.get(user=seller)
#     except SellerProfile.DoesNotExist:
#         seller_profile = None
    
#     if request.method == "POST":
#         form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
#         if form.is_valid():
#             seller_profile = form.save(commit=False)
#             seller_profile.user = seller
#             seller_profile.save()
#             return redirect('users/seller_profile', id=id)  # Redirect to the same page or wherever you want
#     else:
#         form = SellerProfileForm(instance=seller_profile)
    
#     products = Product.objects.filter(seller=seller)
#     context = {
#         'form': form,
#         'seller_profile': seller_profile,
#         'products': products
#     }
    
#     return render(request, 'users/sellerprofile.html', context)