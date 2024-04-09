from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Product, Category, Cart, CartItem, Size
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
from users.models import CustomUser, Event, Favorite, SellerProfile, Profile
from datetime import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404

from users.recommendations import recommend_tshirt_size



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



# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'myapp/detail.html'
#     context_object_name = 'item'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             product = self.get_object()
#             context['item_in_favorites'] = Favorite.objects.filter(user=self.request.user, product=product).exists()
#         return context

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             product_id = self.kwargs['pk']
#             user = request.user
#             product = self.get_object()
#             if 'add_to_favorites' in request.POST:
#                 favorite, created = Favorite.objects.get_or_create(user=user, product=product)
#                 if created:
#                     # Товар успешно добавлен в избранное
#                     return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
#                 else:
#                     # Товар уже находится в избранном
#                     return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
#             elif 'remove_from_favorites' in request.POST:
#                 favorite = Favorite.objects.filter(user=user, product=product).first()
#                 if favorite:
#                     favorite.delete()
#                     # Товар успешно удален из избранного
#                     return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
#                 else:
#                     # Товар не найден в избранном
#                     return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
#         else:
#             # Если пользователь не аутентифицирован, перенаправьте его на страницу входа или куда-то еще
#             return redirect('users:login')  # Замените 'login' на нужный вам URL

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Получение профиля пользователя
            try:
                user_profile = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                user_profile = None
            # Получение рекомендованного размера футболки
            if user_profile:
                recommended_size = recommend_tshirt_size(user_profile)
                context['recommended_tshirt_size'] = recommended_size

            context['user_profile'] = user_profile
            # Добавление рекомендованного размера в контекст
            
            # Проверка, добавлен ли товар в избранное пользователем
            product = self.get_object()
            context['item_in_favorites'] = Favorite.objects.filter(user=self.request.user, product=product).exists()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product_id = self.kwargs['pk']
            user = request.user
            product = self.get_object()
            if 'add_to_favorites' in request.POST:
                favorite, created = Favorite.objects.get_or_create(user=user, product=product)
                if created:
                    # Товар успешно добавлен в избранное
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
                else:
                    # Товар уже находится в избранном
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
            elif 'remove_from_favorites' in request.POST:
                favorite = Favorite.objects.filter(user=user, product=product).first()
                if favorite:
                    favorite.delete()
                    # Товар успешно удален из избранного
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
                else:
                    # Товар не найден в избранном
                    return redirect(reverse('myapp:detail', kwargs={'pk': product_id}))
        else:
            # Если пользователь не аутентифицирован, перенаправьте его на страницу входа или куда-то еще
            return redirect('users:login')  # Замените 'login' на нужный вам URL
        

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
        size_id = request.POST.get("size")  # Получаем выбранный размер из формы
        size = Size.objects.get(pk=size_id)  # Получаем объект размера
        
        item = Product(name=name, price=price, description=description, image=image, seller=seller, category=category)
        item.save()
        item.sizes.add(size)  # Добавляем выбранный размер к товару

    return render(request, "myapp/additem.html", {'categories': categories, 'sizes': sizes})


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

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Получаем размер товара из запроса (если он был передан)
    size_id = request.POST.get('size')
    
    if size_id:
        size = get_object_or_404(Size, pk=size_id)
        
        # Проверяем, есть ли товар в корзине с указанным размером
        cart_item, created = CartItem.objects.get_or_create(product=product, user=user, size=size)
        
        if not created:
            # Если товар уже есть в корзине, увеличиваем его количество на один экземпляр
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Если товара с таким размером еще нет в корзине, создаем новый экземпляр
            cart_item.quantity = 1
            cart_item.save()
            cart.items.add(cart_item)
    
    return redirect('myapp:cart')



@login_required
def cart_view(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    sizes = Size.objects.all()  # Получение всех доступных размеров
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
        # Если количество товара больше одного, уменьшаем его на один экземпляр
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Если количество товара равно одному, удаляем его из корзины
        cart_item.delete()
    return redirect('myapp:cart')

