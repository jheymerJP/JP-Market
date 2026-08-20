from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from .models import Pago, Boleta, Factura, Cupon, Review, Banner, Notificacion
from .forms import CuponForm, BannerForm
from .services import AdminDashboard
from carrito.models import Order, OrderItem
from tienda.models import Product, Category


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('cuentas:login')
        if not request.user.is_staff:
            return redirect('tienda:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    stats = AdminDashboard.get_stats()
    return render(request, 'panel_admin/dashboard.html', stats)


@admin_required
def ventas(request):
    orders = Order.objects.select_related('user').all()
    status = request.GET.get('status', '')
    q = request.GET.get('q', '')
    if status:
        orders = orders.filter(status=status)
    if q:
        orders = orders.filter(Q(order_id__icontains=q) | Q(full_name__icontains=q))

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'cambiar_estado':
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('new_status')
            Order.objects.filter(order_id=order_id).update(status=new_status)
            messages.success(request, f'Pedido {order_id} actualizado a {new_status}')

    return render(request, 'panel_admin/ventas.html', {'orders': orders, 'status': status, 'q': q})


@admin_required
def clientes(request):
    users = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')
    q = request.GET.get('q', '')
    if q:
        users = users.filter(
            Q(username__icontains=q) | Q(email__icontains=q) |
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    return render(request, 'panel_admin/clientes.html', {'users': users, 'q': q})


@admin_required
def cliente_detail(request, user_id):
    user_obj = get_object_or_404(User, id=user_id, is_staff=False)
    orders = Order.objects.filter(user=user_obj).order_by('-created')
    total_gastado = orders.aggregate(t=Sum('total'))['t'] or 0
    return render(request, 'panel_admin/cliente_detail.html', {
        'cliente': user_obj,
        'orders': orders,
        'total_gastado': round(total_gastado, 2),
    })


@admin_required
def productos(request):
    products = Product.objects.select_related('category').all()
    q = request.GET.get('q', '')
    cat = request.GET.get('cat', '')
    if q:
        products = products.filter(name__icontains=q)
    if cat:
        products = products.filter(category_id=cat)
    categories = Category.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        pid = request.POST.get('product_id')
        if action == 'toggle':
            Product.objects.filter(id=pid).update(activo=not Product.objects.get(id=pid).activo)
            messages.success(request, 'Producto actualizado')
        elif action == 'stock':
            stock_val = int(request.POST.get('stock', 0))
            Product.objects.filter(id=pid).update(stock=stock_val)
            messages.success(request, 'Stock actualizado')

    return render(request, 'panel_admin/productos.html', {
        'products': products, 'q': q, 'cat_id': cat, 'categories': categories,
    })


@admin_required
def cupones(request):
    if request.method == 'POST':
        form = CuponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cupon creado!')
            return redirect('panel_admin:cupones')
    else:
        form = CuponForm()
    cupones = Cupon.objects.all()
    return render(request, 'panel_admin/cupones.html', {'cupones': cupones, 'form': form})


@admin_required
def cupon_editar(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    if request.method == 'POST':
        form = CuponForm(request.POST, instance=cupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cupon actualizado!')
            return redirect('panel_admin:cupones')
    else:
        form = CuponForm(instance=cupon)
    return render(request, 'panel_admin/cupon_form.html', {'form': form, 'cupon': cupon})


@admin_required
def cupon_eliminar(request, cupon_id):
    Cupon.objects.filter(id=cupon_id).delete()
    messages.success(request, 'Cupon eliminado')
    return redirect('panel_admin:cupones')


@admin_required
def reviews(request):
    reviews = Review.objects.select_related('user', 'product').all()
    if request.method == 'POST':
        rid = request.POST.get('review_id')
        Review.objects.filter(id=rid).delete()
        messages.success(request, 'Resena eliminada')
    return render(request, 'panel_admin/reviews.html', {'reviews': reviews})


@admin_required
def banners(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner creado!')
            return redirect('panel_admin:banners')
    else:
        form = BannerForm()
    banners = Banner.objects.all()
    return render(request, 'panel_admin/banners.html', {'banners': banners, 'form': form})


@admin_required
def banner_eliminar(request, banner_id):
    Banner.objects.filter(id=banner_id).delete()
    messages.success(request, 'Banner eliminado')
    return render(request, 'panel_admin/banners.html', {'banners': Banner.objects.all(), 'form': BannerForm()})


@admin_required
def boletas(request):
    boletas = Boleta.objects.select_related('order').all()
    return render(request, 'panel_admin/boletas.html', {'boletas': boletas})


@admin_required
def boleta_detail(request, boleta_id):
    boleta = get_object_or_404(Boleta, id=boleta_id)
    items = boleta.order.items.select_related('product').all()
    return render(request, 'panel_admin/boleta_detail.html', {'boleta': boleta, 'items': items})


@admin_required
def facturas(request):
    facturas = Factura.objects.select_related('order').all()
    return render(request, 'panel_admin/facturas.html', {'facturas': facturas})


@admin_required
def factura_detail(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    items = factura.order.items.select_related('product').all()
    return render(request, 'panel_admin/factura_detail.html', {'factura': factura, 'items': items})


@admin_required
def reportes(request):
    stats = AdminDashboard.get_stats()
    return render(request, 'panel_admin/reportes.html', stats)


@admin_required
def config(request):
    return render(request, 'panel_admin/config.html')
