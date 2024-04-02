from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
from users.models import CustomUser, Event
from datetime import datetime



# def index(request):   #ProductListView(ListView):
#     items = Product.objects.all()
#     context = {
#         'items': items
#     }
#     return render(request, "myapp/index.html", context)



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'items'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = Product.objects.all()

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))

        queryset = queryset.filter(seller__is_seller=True)
        queryset = queryset.order_by('id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sellers = CustomUser.objects.filter(is_seller=True)
        events = Event.objects.all()

        # Для ивентов создаем отдельный объект пагинации
        paginator = Paginator(events, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context['sellers'] = sellers
        context['events'] = events
        return context



# def indexItem(request, my_id):   #ProductDetailView(DetailView):
#     item = Product.objects.get(id=my_id)
#     context = {
#         'item': item
#     }
#     return render(request, "myapp/detail.html", context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'item'

@login_required
def add_item(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get('upload')
        seller = request.user
        category_id = request.POST.get("category")  # Добавлено получение категории из формы
        category = Category.objects.get(pk=category_id)
        
        item = Product(name=name, price=price, description=description, image=image, seller=seller, category=category)
        item.save()

    return render(request, "myapp/additem.html", {'categories': categories})

def add_event(request):
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES.get('upload')
        date_str = request.POST.get("date")
        
        # Преобразование строки даты в объект datetime
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        
        organizer = request.user
        item = Event(name=name, image=image, date=date, organizer=organizer)
        item.save()

    return render(request, "myapp/addevent.html")

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

