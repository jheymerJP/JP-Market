from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from carrito.models import Order, OrderItem
from tienda.models import Product, Category
from .models import Pago, Cupon, Review, Notificacion, Banner, Boleta, Factura
from .forms import CuponForm, BannerForm
from .services import AdminDashboard


@staff_member_required(login_url='cuentas:login')
def dashboard(request):
    stats = AdminDashboard.get_stats()
    return render(request, 'panel_admin/dashboard.html', stats)


@staff_member_required(login_url='cuentas:login')
def ventas(request):
    pedidos = Order.objects.select_related('user').all()
    estado = request.GET.get('estado', '')
    busqueda = request.GET.get('q', '')
    if estado:
        pedidos = pedidos.filter(status=estado)
    if busqueda:
        pedidos = pedidos.filter(
            Q(full_name__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(order_id__icontains=busqueda)
        )
    return render(request, 'panel_admin/ventas.html', {
        'pedidos': pedidos,
        'estado_actual': estado,
        'busqueda': busqueda,
    })


@staff_member_required(login_url='cuentas:login')
def pedido_detail(request, order_id):
    pedido = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        pedido.status = request.POST.get('status', pedido.status)
        pedido.save()
        messages.success(request, 'Pedido actualizado exitosamente.')
        return redirect('panel_admin:ventas')
    return render(request, 'panel_admin/pedido_detail.html', {'pedido': pedido})


@staff_member_required(login_url='cuentas:login')
def clientes(request):
    busqueda = request.GET.get('q', '')
    clientes_list = User.objects.filter(is_staff=False).select_related('profile')
    if busqueda:
        clientes_list = clientes_list.filter(
            Q(username__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        )
    total_clientes = User.objects.filter(is_staff=False).count()
    return render(request, 'panel_admin/clientes.html', {
        'clientes': clientes_list,
        'busqueda': busqueda,
        'total_clientes': total_clientes,
    })


@staff_member_required(login_url='cuentas:login')
def cliente_detail(request, user_id):
    cliente = get_object_or_404(User, id=user_id, is_staff=False)
    pedidos = Order.objects.filter(user=cliente)
    total_gastado = pedidos.aggregate(total=Sum('total'))['total'] or 0
    return render(request, 'panel_admin/cliente_detail.html', {
        'cliente': cliente,
        'pedidos': pedidos,
        'total_gastado': total_gastado,
    })


@staff_member_required(login_url='cuentas:login')
def productos(request):
    busqueda = request.GET.get('q', '')
    categoria = request.GET.get('cat', '')
    productos_list = Product.objects.select_related('category').all()
    if busqueda:
        productos_list = productos_list.filter(
            Q(name__icontains=busqueda) | Q(description__icontains=busqueda)
        )
    if categoria:
        productos_list = productos_list.filter(category__slug=categoria)
    categorias = Category.objects.all()
    return render(request, 'panel_admin/productos.html', {
        'productos': productos_list,
        'categorias': categorias,
        'busqueda': busqueda,
        'cat_actual': categoria,
    })


@staff_member_required(login_url='cuentas:login')
def producto_toggle(request, product_id):
    producto = get_object_or_404(Product, id=product_id)
    producto.available = not producto.available
    producto.save()
    return redirect('panel_admin:productos')


@staff_member_required(login_url='cuentas:login')
def cupones(request):
    form = CuponForm()
    cupones_list = Cupon.objects.all()
    if request.method == 'POST':
        form = CuponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cupon creado exitosamente.')
            return redirect('panel_admin:cupones')
    return render(request, 'panel_admin/cupones.html', {
        'cupones': cupones_list,
        'form': form,
    })


@staff_member_required(login_url='cuentas:login')
def cupon_editar(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    if request.method == 'POST':
        form = CuponForm(request.POST, instance=cupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cupon actualizado.')
            return redirect('panel_admin:cupones')
    else:
        form = CuponForm(instance=cupon)
    return render(request, 'panel_admin/cupon_form.html', {'form': form, 'cupon': cupon})


@staff_member_required(login_url='cuentas:login')
def cupon_delete(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    cupon.delete()
    messages.success(request, 'Cupon eliminado.')
    return redirect('panel_admin:cupones')


@staff_member_required(login_url='cuentas:login')
def reviews(request):
    reviews_list = Review.objects.select_related('user', 'product').all()
    return render(request, 'panel_admin/reviews.html', {'reviews': reviews_list})


@staff_member_required(login_url='cuentas:login')
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, 'Resena eliminada.')
    return redirect('panel_admin:reviews')


@staff_member_required(login_url='cuentas:login')
def banners(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner creado.')
            return redirect('panel_admin:banners')
    else:
        form = BannerForm()
    banners_list = Banner.objects.all()
    return render(request, 'panel_admin/banners.html', {
        'banners': banners_list,
        'form': form,
    })


@staff_member_required(login_url='cuentas:login')
def boletas(request):
    boletas_list = Boleta.objects.all()
    return render(request, 'panel_admin/boletas.html', {'boletas': boletas_list})


@staff_member_required(login_url='cuentas:login')
def boleta_detail(request, boleta_id):
    boleta = get_object_or_404(Boleta, id=boleta_id)
    items = OrderItem.objects.filter(order=boleta.order)
    return render(request, 'panel_admin/boleta_detail.html', {'boleta': boleta, 'items': items})


@staff_member_required(login_url='cuentas:login')
def facturas(request):
    facturas_list = Factura.objects.all()
    return render(request, 'panel_admin/facturas.html', {'facturas': facturas_list})


@staff_member_required(login_url='cuentas:login')
def factura_detail(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    items = OrderItem.objects.filter(order=factura.order)
    return render(request, 'panel_admin/factura_detail.html', {'factura': factura, 'items': items})


@staff_member_required(login_url='cuentas:login')
def generar_boleta(request, order_id):
    pedido = get_object_or_404(Order, order_id=order_id)
    if Boleta.objects.filter(order=pedido).exists():
        messages.warning(request, 'Ya existe una boleta para este pedido.')
        return redirect('panel_admin:boletas')
    subtotal = pedido.total
    iva = subtotal * 0.19
    boleta = Boleta.objects.create(
        order=pedido,
        cliente_nombre=pedido.full_name,
        cliente_email=pedido.email,
        cliente_direccion=pedido.address,
        cliente_ciudad=pedido.city,
        cliente_documento=request.POST.get('documento', ''),
        subtotal=subtotal,
        iva=iva,
        total=subtotal + iva,
        metodo_pago=request.POST.get('metodo_pago', 'No especificado'),
    )
    messages.success(request, f'Boleta {boleta.numero} generada.')
    return redirect('panel_admin:boleta_detail', boleta_id=boleta.id)


@staff_member_required(login_url='cuentas:login')
def generar_factura(request, order_id):
    pedido = get_object_or_404(Order, order_id=order_id)
    if Factura.objects.filter(order=pedido).exists():
        messages.warning(request, 'Ya existe una factura para este pedido.')
        return redirect('panel_admin:facturas')
    subtotal = pedido.total
    iva = subtotal * 0.19
    factura = Factura.objects.create(
        order=pedido,
        cliente_nombre=pedido.full_name,
        cliente_email=pedido.email,
        cliente_direccion=pedido.address,
        cliente_ciudad=pedido.city,
        cliente_nit=request.POST.get('nit', '000000000'),
        subtotal=subtotal,
        iva=iva,
        total=subtotal + iva,
        metodo_pago=request.POST.get('metodo_pago', 'No especificado'),
    )
    messages.success(request, f'Factura {factura.numero} generada.')
    return redirect('panel_admin:factura_detail', factura_id=factura.id)


@staff_member_required(login_url='cuentas:login')
def reportes(request):
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_año = hoy.replace(month=1, day=1)

    ventas_hoy = Pago.objects.filter(estado='approved', created__date=hoy).aggregate(t=Sum('monto'))['t'] or 0
    ventas_mes = Pago.objects.filter(estado='approved', created__date__gte=inicio_mes).aggregate(t=Sum('monto'))['t'] or 0
    ventas_año = Pago.objects.filter(estado='approved', created__date__gte=inicio_año).aggregate(t=Sum('monto'))['t'] or 0

    pedidos_hoy = Order.objects.filter(created__date=hoy).count()
    pedidos_mes = Order.objects.filter(created__date__gte=inicio_mes).count()
    pedidos_pendientes = Order.objects.filter(status='pending').count()

    clientes_nuevos_mes = User.objects.filter(is_staff=False, date_joined__gte=inicio_mes).count()
    clientes_total = User.objects.filter(is_staff=False).count()

    productos_total = Product.objects.count()
    productos_stock_bajo = Product.objects.filter(stock__lte=5, stock__gt=0).count()
    productos_agotados = Product.objects.filter(stock=0).count()

    ticket_promedio = Pago.objects.filter(
        estado='approved', created__date__gte=inicio_mes
    ).aggregate(t=Avg('monto'))['t'] or 0

    top_productos = Product.objects.annotate(
        vendidos=Count('orderitem')
    ).order_by('-vendidos')[:10]

    ventas_por_categoria = Category.objects.annotate(
        total_ventas=Sum('products__orderitem__price')
    ).order_by('-total_ventas')

    pedidos_por_estado = Order.objects.values('status').annotate(
        total=Count('id')
    )

    top_ciudades = Order.objects.values('city').annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    pagos_por_metodo = Pago.objects.filter(
        estado='approved'
    ).values('metodo_pago').annotate(
        total=Sum('monto'),
        cantidad=Count('id')
    ).order_by('-total')

    report_data = {
        'ventas_hoy': ventas_hoy,
        'ventas_mes': ventas_mes,
        'ventas_año': ventas_año,
        'pedidos_hoy': pedidos_hoy,
        'pedidos_mes': pedidos_mes,
        'pedidos_pendientes': pedidos_pendientes,
        'clientes_nuevos_mes': clientes_nuevos_mes,
        'clientes_total': clientes_total,
        'productos_total': productos_total,
        'productos_stock_bajo': productos_stock_bajo,
        'productos_agotados': productos_agotados,
        'ticket_promedio': ticket_promedio,
        'top_productos': top_productos,
        'ventas_por_categoria': ventas_por_categoria,
        'pedidos_por_estado': pedidos_por_estado,
        'top_ciudades': top_ciudades,
        'pagos_por_metodo': pagos_por_metodo,
    }

    return render(request, 'panel_admin/reportes.html', report_data)


from django.db.models import Avg


@staff_member_required(login_url='cuentas:login')
def config(request):
    if request.method == 'POST':
        messages.success(request, 'Configuracion guardada.')
        return redirect('panel_admin:config')
    return render(request, 'panel_admin/config.html')
