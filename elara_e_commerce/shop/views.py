from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem, Order, OrderItem, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

#Function to see the categorys
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html',{'categories':categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category_detail.html',{'category':category, 'products':products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html',{'products':products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html',{'product':product})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/cart_detail.html', {'cart_item': cart_item, 'cart':cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'price': product.price,
            'quantity': 1
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart_user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_list.html', {'orders':orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_item = OrderItem.objects.filter(order=order)
    return render(request, 'shop/order_detail.html',{'order_item':order_item, 'order':order})

@login_required
def shipping_address(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        
        ShippingAddress.objects.update_or_create(
            order__user=request.user,
            defaults={
                'address': address,
                'city': city,
                'postal_code': postal_code,
                'country': country
            }
        )
        return redirect('order_list')
    
    return render(request, 'shop/shipping_address.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('product_list')

    return render(request, 'shop/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'shop/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

