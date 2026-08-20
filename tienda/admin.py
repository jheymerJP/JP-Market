from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'activa', 'created']
    search_fields = ['name']
    list_filter = ['activa']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'activo', 'created']
    list_filter = ['activo', 'category']
    list_editable = ['price', 'stock', 'activo']
    search_fields = ['name', 'description']
