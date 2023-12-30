from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
from users.models import CustomUser


def index(request):   #ProductListView(ListView):
    items = Product.objects.all()
    context = {
        'items': items
    }
    return render(request, "myapp/index.html", context)



class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'items'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = Product.objects.all()

        if query:
            # Используйте Q-объекты для выполнения поиска в нескольких полях модели Product.
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))

        # Отфильтровать только тех продавцов, у которых is_seller=True
        queryset = queryset.filter(seller__is_seller=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получить список продавцов
        sellers = CustomUser.objects.filter(is_seller=True)

        context['sellers'] = sellers
        return context


def indexItem(request, my_id):   #ProductDetailView(DetailView):
    item = Product.objects.get(id=my_id)
    context = {
        'item': item
    }
    return render(request, "myapp/detail.html", context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'item'

@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get('upload')
        seller = request.user
        item = Product(name=name, price=price, description=description, image=image, seller=seller)
        item.save()

    return render(request, "myapp/additem.html")

def update_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get('upload', item.image)
        item.save()
        return redirect("/")

    context = {'item': item}
    return render(request, "myapp/updateitem.html", context)

def delete_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect("/")

    context = {'item': item}
    return render(request, "myapp/deleteitem.html", context)

