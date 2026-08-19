from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('agregar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('eliminar/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('actualizar/<int:item_id>/', views.update_cart, name='update_cart'),
    path('pago/', views.checkout, name='checkout'),
    path('pedido/<uuid:order_id>/', views.order_complete, name='order_complete'),
    path('mis-pedidos/', views.order_history, name='order_history'),
]
