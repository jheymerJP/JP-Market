from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.product_list, name='product_list'),
    path('categorias/', views.category_list, name='category_list'),
    path('categoria/<slug:slug>/', views.category_detail, name='category_detail'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
]
