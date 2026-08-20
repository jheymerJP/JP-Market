from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem
from tienda.models import Product
from panel_admin.models import Pago, Boleta, Factura, Cupon
from django.utils import timezone
import uuid


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        key = request.session.session_key
        if not key:
            request.session.create()
            key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=key)
    return cart


def cart_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    subtotal = cart.total
    descuento = 0
    total = subtotal
    cupon_msg = None

    if request.session.get('cupon_codigo'):
        try:
            cupon = Cupon.objects.get(codigo=request.session['cupon_codigo'], activo=True)
            if cupon.esta_disponible and subtotal >= cupon.minimo_compra:
                descuento = round(subtotal * cupon.descuento / 100, 2)
                total = round(subtotal - descuento, 2)
                cupon_msg = f"Cupon {cupon.codigo} aplicado: -S/.{descuento}"
            else:
                del request.session['cupon_codigo']
                cupon_msg = "Cupon expirado o no valido"
        except Cupon.DoesNotExist:
            del request.session['cupon_codigo']

    return render(request, 'carrito/cart.html', {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'descuento': descuento,
        'total': total,
        'cupon_msg': cupon_msg,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, activo=True)
    cart = get_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'{product.name} agregado al carrito')
    return redirect('carrito:cart')


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('carrito:cart')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('carrito:cart')


def apply_coupon(request):
    if request.method == 'POST':
        codigo = request.POST.get('coupon_code', '').strip().upper()
        try:
            cupon = Cupon.objects.get(codigo=codigo, activo=True)
            if cupon.esta_disponible:
                request.session['cupon_codigo'] = codigo
                messages.success(request, f'Cupon {codigo} aplicado: {cupon.descuento}% de descuento')
            else:
                messages.error(request, 'Cupon agotado o expirado')
        except Cupon.DoesNotExist:
            messages.error(request, 'Cupon no valido')
    return redirect('carrito:cart')


def remove_coupon(request):
    if 'cupon_codigo' in request.session:
        del request.session['cupon_codigo']
        messages.success(request, 'Cupon removido')
    return redirect('carrito:cart')


@login_required
def checkout_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    subtotal = cart.total
    descuento = 0
    total = subtotal

    if request.session.get('cupon_codigo'):
        try:
            cupon = Cupon.objects.get(codigo=request.session['cupon_codigo'], activo=True)
            if cupon.esta_disponible and subtotal >= cupon.minimo_compra:
                descuento = round(subtotal * cupon.descuento / 100, 2)
                total = round(subtotal - descuento, 2)
        except Cupon.DoesNotExist:
            pass

    if not items.exists():
        messages.warning(request, 'Tu carrito esta vacio')
        return redirect('carrito:cart')

    if request.method == 'POST':
        tipo_comprobante = request.POST.get('tipo_comprobante', 'boleta')
        numero_documento = request.POST.get('numero_documento', '').strip()
        razon_social = request.POST.get('razon_social', '').strip()

        if tipo_comprobante == 'boleta':
            if not numero_documento or len(numero_documento) != 8:
                messages.error(request, 'El DNI debe tener 8 digitos')
                return render(request, 'carrito/checkout.html', _ctx(cart, items, subtotal, descuento, total))
            tipo_doc = 'dni'
        else:
            if not numero_documento or len(numero_documento) != 11:
                messages.error(request, 'El RUC debe tener 11 digitos')
                return render(request, 'carrito/checkout.html', _ctx(cart, items, subtotal, descuento, total))
            if not razon_social:
                messages.error(request, 'La Razon Social es obligatoria para factura')
                return render(request, 'carrito/checkout.html', _ctx(cart, items, subtotal, descuento, total))
            tipo_doc = 'ruc'

        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        distrito = request.POST.get('distrito', '').strip()
        phone = request.POST.get('phone', '').strip()
        metodo_pago = request.POST.get('metodo_pago', '')
        notas = request.POST.get('notas', '').strip()

        if not all([full_name, email, address, city, phone]):
            messages.error(request, 'Completa todos los campos obligatorios')
            return render(request, 'carrito/checkout.html', _ctx(cart, items, subtotal, descuento, total))

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=f"{address}, {distrito}" if distrito else address,
            city=city,
            phone=phone,
            tipo_documento=tipo_doc,
            numero_documento=numero_documento,
            tipo_comprobante=tipo_comprobante,
            razon_social=razon_social,
            total=total,
            notas=notas,
            order_id=str(uuid.uuid4())[:10].upper(),
        )

        for ci in items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                price=ci.product.price,
                quantity=ci.quantity,
            )
            ci.product.stock = max(0, ci.product.stock - ci.quantity)
            ci.product.save()

        Pago.objects.create(
            user=request.user,
            order_id=order.order_id,
            metodo_pago=metodo_pago,
            monto=total,
            estado='approved',
        )

        igv = round(total - round(total / 1.18, 2), 2)
        subtotal_neto = round(total - igv, 2)

        if tipo_comprobante == 'boleta':
            Boleta.objects.create(
                order=order,
                cliente_nombre=full_name,
                cliente_email=email,
                cliente_direccion=f"{address}, {distrito}" if distrito else address,
                cliente_ciudad=city,
                cliente_documento=numero_documento,
                subtotal=subtotal_neto,
                igv=igv,
                descuento=descuento,
                total=total,
                metodo_pago=metodo_pago,
                estado='pagada',
            )
        else:
            Factura.objects.create(
                order=order,
                cliente_nombre=razon_social,
                cliente_email=email,
                cliente_direccion=f"{address}, {distrito}" if distrito else address,
                cliente_ciudad=city,
                cliente_nit=numero_documento,
                subtotal=subtotal_neto,
                igv=igv,
                descuento=descuento,
                total=total,
                metodo_pago=metodo_pago,
                estado='pagada',
            )

        cart.items.all().delete()
        if 'cupon_codigo' in request.session:
            del request.session['cupon_codigo']

        return redirect('carrito:order_complete', order_id=order.order_id)

    ctx = _ctx(cart, items, subtotal, descuento, total)
    return render(request, 'carrito/checkout.html', ctx)


def _ctx(cart, items, subtotal, descuento, total):
    return {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'descuento': descuento,
        'total': total,
        'metodos_pago': Pago.METODOS,
    }


def order_complete_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    boleta = Boleta.objects.filter(order=order).first()
    factura = Factura.objects.filter(order=order).first()
    return render(request, 'carrito/order_complete.html', {
        'order': order,
        'boleta': boleta,
        'factura': factura,
    })


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'carrito/order_history.html', {'orders': orders})


@login_required
def order_tracking_public_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.user != order.user and not request.user.is_staff:
        messages.error(request, 'No tienes acceso a este pedido')
        return redirect('tienda:home')
    return render(request, 'carrito/tracking.html', {'order': order})


def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        key = request.session.session_key
        cart = Cart.objects.filter(session_key=key).first() if key else None
    if cart:
        count = cart.total_items
    return {'cart_count': count}
