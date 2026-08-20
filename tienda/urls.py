from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.product_list, name='product_list'),
    path('categorias/', views.category_list, name='category_list'),
    path('categoria/<int:category_id>/', views.category_detail, name='category_detail'),
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),
]
