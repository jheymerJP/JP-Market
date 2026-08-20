from django.db import models
from django.contrib.auth.models import User
from .models import Pago
from tienda.models import Product, Category
from carrito.models import Order
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta


class AdminDashboard:
    @staticmethod
    def get_stats():
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        inicio_semana = hoy - timedelta(days=hoy.weekday())

        ventas_hoy = Pago.objects.filter(
            estado='approved', created__date=hoy
        ).aggregate(total=Sum('monto'))['total'] or 0

        ventas_mes = Pago.objects.filter(
            estado='approved', created__date__gte=inicio_mes
        ).aggregate(total=Sum('monto'))['total'] or 0

        ventas_semana = Pago.objects.filter(
            estado='approved', created__date__gte=inicio_semana
        ).aggregate(total=Sum('monto'))['total'] or 0

        pedidos_hoy = Order.objects.filter(created__date=hoy).count()
        pedidos_pendientes = Order.objects.filter(status='pending').count()
        pedidos_procesando = Order.objects.filter(status='processing').count()
        total_pedidos = Order.objects.count()

        total_clientes = User.objects.filter(is_staff=False).count()
        clientes_nuevos = User.objects.filter(
            is_staff=False, date_joined__gte=inicio_mes
        ).count()

        total_productos = Product.objects.count()
        productos_stock_bajo = Product.objects.filter(stock__lte=5, stock__gt=0).count()
        productos_agotados = Product.objects.filter(stock=0).count()
        total_categorias = Category.objects.count()

        ventas_por_mes = []
        for i in range(5, -1, -1):
            fecha = hoy - timedelta(days=30 * i)
            mes_inicio = fecha.replace(day=1)
            if fecha.month == 12:
                mes_fin = mes_inicio.replace(year=mes_inicio.year + 1, month=1)
            else:
                mes_fin = mes_inicio.replace(month=mes_inicio.month + 1)
            total = Pago.objects.filter(
                estado='approved',
                created__gte=mes_inicio,
                created__lt=mes_fin
            ).aggregate(total=Sum('monto'))['total'] or 0
            ventas_por_mes.append({
                'mes': mes_inicio.strftime('%b %Y'),
                'total': float(total)
            })

        top_productos = Product.objects.annotate(
            vendidos=Count('orderitem')
        ).order_by('-vendidos')[:5]

        pedidos_recientes = Order.objects.select_related('user').all()[:10]

        return {
            'ventas_hoy': ventas_hoy,
            'ventas_mes': ventas_mes,
            'ventas_semana': ventas_semana,
            'pedidos_hoy': pedidos_hoy,
            'pedidos_pendientes': pedidos_pendientes,
            'pedidos_procesando': pedidos_procesando,
            'total_pedidos': total_pedidos,
            'total_clientes': total_clientes,
            'clientes_nuevos': clientes_nuevos,
            'total_productos': total_productos,
            'productos_stock_bajo': productos_stock_bajo,
            'productos_agotados': productos_agotados,
            'total_categorias': total_categorias,
            'ventas_por_mes': ventas_por_mes,
            'top_productos': top_productos,
            'pedidos_recientes': pedidos_recientes,
        }
