from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('agregar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('actualizar/<int:item_id>/', views.update_cart, name='update_cart'),
    path('eliminar/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cupon/', views.apply_coupon, name='apply_coupon'),
    path('cupon/remover/', views.remove_coupon, name='remove_coupon'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido/<str:order_id>/', views.order_complete_view, name='order_complete'),
    path('mis-pedidos/', views.order_history_view, name='order_history'),
    path('rastrear/<str:order_id>/', views.order_tracking_public_view, name='tracking'),
]
