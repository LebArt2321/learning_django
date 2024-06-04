from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Product, Category, Cart, CartItem, Size, ProductSize, Order, OrderItem
from users.models import CustomUser, Event, Favorite,  Profile
from users.recommendations import recommend_tshirt_size, recommend_sweatshirt_size, recommend_pants_size
from django.contrib import messages

def autocomplete_search(request):
    query = request.GET.get('term', '')
    product_results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).values_list('name', flat=True)
    event_results = Event.objects.filter(name__icontains=query).values_list('name', flat=True)
    
    results = list(product_results) + list(event_results)
    return JsonResponse(results, safe=False)

class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        filters = self.request.GET.get('filters', '')
        categories = self.request.GET.getlist('category')
        filters_list = filters.split(',') if filters else []

        queryset = Product.objects.all()

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
            filters_list = [query]

        if filters_list:
            for filter in filters_list:
                queryset = queryset.filter(Q(name__icontains=filter) | Q(description__icontains=filter))

        if categories:
            queryset = queryset.filter(category__name__in=categories)

        queryset = queryset.filter(seller__is_seller=True)
        queryset = queryset.order_by('id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sellers = CustomUser.objects.filter(is_seller=True)
        events = Event.objects.all()
        categories = Category.objects.all()

        paginator = Paginator(events, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        filters = self.request.GET.get('filters', '')
        filters_list = [f for f in filters.split(',') if f]

        selected_categories = self.request.GET.getlist('category')

        context['sellers'] = sellers
        context['events'] = events
        context['filters'] = filters
        context['filters_list'] = filters_list
        context['categories'] = categories
        context['selected_categories'] = selected_categories

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        available_sizes = product.product_sizes.filter(quantity_available__gt=0)
        context['available_sizes'] = available_sizes
        
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                user_profile = None

            recommended_size = None

            if user_profile:
                if product.category.name == 'Футболка' and user_profile.height and user_profile.chest_circumference and user_profile.waist_circumference:
                    recommended_size = recommend_tshirt_size(user_profile)
                elif product.category.name == 'Толстовка' and user_profile.chest_circumference and user_profile.waist_circumference and user_profile.hip_girth and user_profile.shoulder_width and user_profile.height:
                    recommended_size = recommend_sweatshirt_size(user_profile)
                elif product.category.name == 'Штаны' and user_profile.waist_circumference and user_profile.hip_girth and user_profile.pants_length:
                    recommended_size = recommend_pants_size(user_profile)
            context['recommended_size'] = recommended_size
            context['user_profile'] = user_profile

            item_in_favorites = Favorite.objects.filter(user=self.request.user, product=product).exists()
            context['item_in_favorites'] = item_in_favorites
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product_id = self.kwargs['pk']
            user = request.user
            product = self.get_object()
            if 'add_to_favorites' in request.POST:
                favorite, created = Favorite.objects.get_or_create(user=user, product=product)
                if created:
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
                else:
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
            elif 'remove_from_favorites' in request.POST:
                favorite = Favorite.objects.filter(user=user, product=product).first()
                if favorite:
                    favorite.delete()
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
                else:
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
        else:
            return redirect('users:login')


@login_required
def add_item(request):
    categories = Category.objects.all()
    sizes = Size.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get('upload')
        seller = request.user
        category_id = request.POST.get("category")
        category = Category.objects.get(pk=category_id)
        
        item = Product(name=name, price=price, description=description, image=image, seller=seller, category=category)
        item.save()
        
        size_id = request.POST.get("size")
        quantity = request.POST.get("quantity")
        size = Size.objects.get(pk=size_id)
        
        product_size = ProductSize(product=item, size=size, quantity_available=quantity)
        product_size.save()
        
        return redirect("/")

    return render(request, "myapp/additem.html", {'categories': categories, 'sizes': sizes})


def add_event(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get('upload')
        date_str = request.POST.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        organizer = request.user
        item = Event(name=name, image=image, description= description, date=date, organizer=organizer)
        item.save()
        return redirect("/")

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductSize, Cart, CartItem, Order, OrderItem

@login_required
def add_to_cart(request, product_size_id):
    product_size = get_object_or_404(ProductSize, pk=product_size_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(product_size=product_size, user=user)

    if product_size.quantity_available > cart_item.quantity:
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
            cart_item.save()
            cart.items.add(cart_item)
    else:
        messages.error(request, 'Извините, больше нет доступных товаров этого размера.')

    return redirect('myapp:cart')

@login_required
def cart_view(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    sizes = Size.objects.all()
    return render(request, 'myapp/cart.html', {'cart': cart, 'sizes': sizes})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('myapp:cart')

@login_required
def remove_single_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('myapp:cart')

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        total_price = cart.total()
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_size=item.product_size,
                quantity=item.quantity,
                price=item.product_size.product.price
            )
            item.product_size.quantity_available -= item.quantity
            item.product_size.save()
        # Удаляем каждый элемент корзины вручную
        cart.items.all().delete()
        return redirect('myapp:order_history')
    return render(request, 'myapp/place_order.html', {'cart': cart})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'myapp/order_history.html', {'orders': orders})
