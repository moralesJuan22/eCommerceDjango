from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .cart import Cart
from django.views.decorators.http import require_POST
from .forms import OrderCreateForm, UserRegistrationForm
from .models import OrderItem
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart.add(product=product, quantity=1)
    return redirect('product_list') 

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(product_id=product_id, quantity=quantity)
    return redirect('cart_detail')

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def order_history(request):
    orders = request.user.orders.all()
    return render(request, 'store/order_history.html', {'orders': orders})