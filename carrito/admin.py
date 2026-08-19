from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total', 'total_items', 'created']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'full_name', 'email', 'city', 'total', 'status', 'created']
    list_filter = ['status', 'city']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id', 'user', 'full_name', 'email', 'address', 'city', 'phone', 'total', 'created']
