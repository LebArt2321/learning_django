from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import CustomUser





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
    if request.method == "POST":
        contact_number = request.POST.get("contact_number")
        image = request.FILES.get('upload')
        user = request.user
        person = Profile(user=user,contact_number=contact_number, image=image)
        person.save()
    return render(request, 'users/profile.html')



def seller_profile(request, id):
    seller = CustomUser.objects.get(id=id)
    
    context = {
        'seller': seller
    }
    
    return render(request, 'users/sellerprofile.html', context)
