from django.urls import path
from . import views

app_name = 'panel_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/<uuid:order_id>/', views.pedido_detail, name='pedido_detail'),
    path('ventas/<uuid:order_id>/generar-boleta/', views.generar_boleta, name='generar_boleta'),
    path('ventas/<uuid:order_id>/generar-factura/', views.generar_factura, name='generar_factura'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:user_id>/', views.cliente_detail, name='cliente_detail'),
    path('productos/', views.productos, name='productos'),
    path('productos/<int:product_id>/toggle/', views.producto_toggle, name='producto_toggle'),
    path('cupones/', views.cupones, name='cupones'),
    path('cupones/<int:cupon_id>/editar/', views.cupon_editar, name='cupon_editar'),
    path('cupones/<int:cupon_id>/eliminar/', views.cupon_delete, name='cupon_delete'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/<int:review_id>/eliminar/', views.review_delete, name='review_delete'),
    path('banners/', views.banners, name='banners'),
    path('boletas/', views.boletas, name='boletas'),
    path('boletas/<int:boleta_id>/', views.boleta_detail, name='boleta_detail'),
    path('facturas/', views.facturas, name='facturas'),
    path('facturas/<int:factura_id>/', views.factura_detail, name='factura_detail'),
    path('reportes/', views.reportes, name='reportes'),
    path('configuracion/', views.config, name='config'),
]
