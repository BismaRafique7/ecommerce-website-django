from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, CartItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm
from .models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from .cart import Cart  
from .models import Product, Category
from django.utils import timezone


# store/views.py
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)
def update_cart_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        current_quantity = 0
        for item in cart:
            if item['product'].id == product.id:
                current_quantity = item['quantity']
                break

        if action == 'increase':
            new_quantity = current_quantity + 1
        elif action == 'decrease':
            new_quantity = max(1, current_quantity - 1)  
        else:
            new_quantity = current_quantity

        cart.add(product=product, quantity=new_quantity, update_quantity=True)

    return redirect('cart')


   
def is_admin(user):
    return user.is_superuser



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home')

    return render(request, "register.html", {"auth_page": True})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')

    return render(request, "login.html", {"auth_page": True})



def logout_view(request):
    logout(request)
    return redirect('login')




def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('cart')




@login_required
#def cart_view(request):
 #   cart_items = CartItem.objects.filter(user=request.user)
  #  total = sum([item.product.price * item.quantity for item in cart_items])
  #  for item in cart_items:
   #     item.total_price = item.product.price * item.quantity
   # return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def cart_view(request):
    cart = Cart(request)
    cart_items = list(cart)  # cart ke items ko list mein convert
    total = sum(item['product'].price * item['quantity'] for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def place_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cart')

        order = Order.objects.create(user=request.user, address=address)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart_items.delete()
        return redirect('user_orders')

    return redirect('cart')


@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin_orders.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST['status']
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        return redirect('admin_orders')

def home(request):
    return render(request, 'home.html')
@login_required
def remove_from_cart(request, product_id):
    try:
        item = CartItem.objects.get(user=request.user, product_id=product_id)
        item.delete()
        messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')

    return redirect('cart')

@login_required
def checkout_view(request):
    cart = Cart(request)
    return render(request, 'checkout.html', {'cart_items': list(cart)})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})
@staff_member_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'add_product.html', {'form': form})


@staff_member_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('admin_products')

@staff_member_required
def admin_products(request):
    products = Product.objects.all()
    return render(request, 'admin_products.html', {'products': products})
@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user_orders.html', {'orders': orders})

@login_required
def confirm_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        cart = request.session.get('cart', {})

        if not cart:
            return redirect('cart')  

        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address
        )

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price  
            )

        request.session['cart'] = {}  
        
        return redirect('order_success', order_id=order.id)
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('checkout')  # checkout ka URL name
#def frontpage(request):
 #   categories = Category.objects.all()
 #   new_products = Product.objects.order_by('-created_at')[:8]
 #   sale_products = Product.objects.filter(sale_price__isnull=False, sale_end__gte=timezone.now())[:8]
  #  return render(request, 'frontpage.html', {
 #       'categories': categories,
 #       'new_products': new_products,
 #       'sale_products': sale_products,
#        'year': timezone.now().year
#    })
#def category_products(request, slug):
   # category = get_object_or_404(Category, slug=slug)
   # products = Product.objects.filter(category=category)
   # return render(request, 'category_products.html', {'category': category, 'products': products})
def frontpage(request):
    categories = Category.objects.all()
    new_products = Product.objects.order_by('-created_at')[:8]
    now = timezone.now()
    sale_products = Product.objects.filter(
        sale_price__isnull=False,
        sale_price__lt=models.F('price')
    ).filter(
        Q(sale_start__lte=now) | Q(sale_start__isnull=True),
        Q(sale_end__gte=now) | Q(sale_end__isnull=True)
    )[:4]

    fragrance_products = Product.objects.filter(category__slug='fragrance')[:4]

    clothes_products = Product.objects.filter(category__slug='clothes')[:4]
    return render(request, 'frontpage.html', {
        'categories': categories,
        'new_products': new_products,
        'sale_products': sale_products,
        'fragrance_products': fragrance_products,
        'clothes_products': clothes_products
    })



def category(request, foo):
    category = get_object_or_404(Category, slug=foo)
    products = Product.objects.filter(category=category)

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})
def search_view(request):
    query = request.GET.get('q', '')
    products = []

    if query:
        
        category = Category.objects.filter(name__icontains=query).first()
        if category:
            products = Product.objects.filter(category=category)
        else:
          
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    return render(request, 'search_results.html', {
        'query': query,
        'products': products,
    })
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })