from django.urls import path
from . import views

app_name = 'panel_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ventas/', views.ventas, name='ventas'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:user_id>/', views.cliente_detail, name='cliente_detail'),
    path('productos/', views.productos, name='productos'),
    path('cupones/', views.cupones, name='cupones'),
    path('cupones/<int:cupon_id>/editar/', views.cupon_editar, name='cupon_editar'),
    path('cupones/<int:cupon_id>/eliminar/', views.cupon_eliminar, name='cupon_eliminar'),
    path('resenas/', views.reviews, name='reviews'),
    path('banners/', views.banners, name='banners'),
    path('banners/<int:banner_id>/eliminar/', views.banner_eliminar, name='banner_eliminar'),
    path('boletas/', views.boletas, name='boletas'),
    path('boletas/<int:boleta_id>/', views.boleta_detail, name='boleta_detail'),
    path('facturas/', views.facturas, name='facturas'),
    path('facturas/<int:factura_id>/', views.factura_detail, name='factura_detail'),
    path('reportes/', views.reportes, name='reportes'),
    path('configuracion/', views.config, name='config'),
]
