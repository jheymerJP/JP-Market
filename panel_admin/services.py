from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from carrito.models import Order, OrderItem
from panel_admin.models import Pago, Cupon
from tienda.models import Product, Category
from django.contrib.auth.models import User


class AdminDashboard:

    @staticmethod
    def get_stats():
        now = timezone.localtime(timezone.now())
        mes_inicio = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ayer = now - timedelta(days=1)

        pedidos_mes = Order.objects.filter(created__gte=mes_inicio)
        pedidos_hoy = Order.objects.filter(created__date=now.date())

        ventas_mes = pedidos_mes.aggregate(t=Sum('total'))['t'] or 0
        ventas_hoy = pedidos_hoy.aggregate(t=Sum('total'))['t'] or 0
        pedidos_total_mes = pedidos_mes.count()
        clientes_nuevos = User.objects.filter(is_staff=False, date_joined__gte=mes_inicio).count()
        stock_total = Product.objects.filter(activo=True).aggregate(t=Sum('stock'))['t'] or 0
        ticket_promedio = pedidos_mes.aggregate(a=Avg('total'))['a'] or 0

        pedidos_recientes = Order.objects.select_related('user')[:10]
        top_products = (
            OrderItem.objects.filter(order__created__gte=mes_inicio)
            .values('product__name')
            .annotate(cantidad=Count('id'), total_vendido=Sum('price'))
            .order_by('-cantidad')[:10]
        )

        metodos_pago = (
            Pago.objects.filter(created__gte=mes_inicio)
            .values('metodo_pago')
            .annotate(total=Sum('monto'), cantidad=Count('id'))
            .order_by('-total')
        )

        ventas_por_mes = (
            Order.objects.filter(created__gte=now - timedelta(days=365))
            .annotate(mes=TruncMonth('created'))
            .values('mes')
            .annotate(total=Sum('total'), cantidad=Count('id'))
            .order_by('mes')
        )

        cities_stats = (
            Order.objects.filter(created__gte=mes_inicio)
            .values('city')
            .annotate(total=Sum('total'), cantidad=Count('id'))
            .order_by('-total')[:10]
        )

        pedidos_por_status = (
            Order.objects.filter(created__gte=mes_inicio)
            .values('status')
            .annotate(cantidad=Count('id'))
        )

        categorias = Category.objects.annotate(cantidad=Count('products')).order_by('-cantidad')

        return {
            'ventas_mes': round(ventas_mes, 2),
            'ventas_hoy': round(ventas_hoy, 2),
            'pedidos_mes': pedidos_total_mes,
            'clientes_nuevos': clientes_nuevos,
            'stock_total': stock_total,
            'ticket_promedio': round(ticket_promedio, 2),
            'pedidos_recientes': pedidos_recientes,
            'top_products': top_products,
            'metodos_pago': metodos_pago,
            'ventas_por_mes': list(ventas_por_mes),
            'cities_stats': cities_stats,
            'pedidos_por_status': list(pedidos_por_status),
            'categorias': categorias,
            'now': now,
            'mes_inicio': mes_inicio,
        }
