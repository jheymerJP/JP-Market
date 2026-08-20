from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from tienda.models import Product
import uuid


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, 'No hay suficiente stock disponible.')
    else:
        cart_item.quantity = 1
        cart_item.save()
    messages.success(request, f'"{product.name}" agregado al carrito.')
    return redirect('carrito:cart_detail')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito:cart_detail')


def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if 0 < quantity <= cart_item.product.stock:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        messages.warning(request, 'Cantidad no valida.')
    return redirect('carrito:cart_detail')


def cart_detail(request):
    cart = get_cart(request)
    items = cart.items.select_related('product')
    return render(request, 'carrito/cart.html', {
        'cart': cart,
        'items': items,
    })


@login_required
def checkout(request):
    cart = get_cart(request)
    items = cart.items.select_related('product')
    if not items.exists():
        messages.warning(request, 'Tu carrito esta vacio.')
        return redirect('tienda:home')

    if request.method == 'POST':
        from panel_admin.models import Pago

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        metodo_pago = request.POST.get('metodo_pago', 'credit_card')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            phone=phone,
            total=cart.total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )
            product = item.product
            product.stock -= item.quantity
            product.save()

        Pago.objects.create(
            user=request.user,
            order_id=str(order.order_id),
            metodo_pago=metodo_pago,
            monto=cart.total,
            estado='approved' if metodo_pago != 'efectivo' else 'pending',
            referencia=f'Pago {metodo_pago} - {order.order_id}',
        )

        cart.items.all().delete()
        messages.success(request, 'Pedido realizado exitosamente!')
        return redirect('carrito:order_complete', order_id=order.order_id)

    return render(request, 'carrito/checkout.html', {
        'cart': cart,
        'items': items,
    })


@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'carrito/order_complete.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'carrito/order_history.html', {'orders': orders})
