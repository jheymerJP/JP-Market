from django.contrib import admin
from .models import Pago, Cupon, Review, Notificacion, Banner


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'metodo_pago', 'monto', 'estado', 'created']
    list_filter = ['estado', 'metodo_pago']
    list_editable = ['estado']
    search_fields = ['order_id', 'referencia']


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descuento', 'activo', 'uso_actual', 'uso_maximo', 'minimo_compra']
    list_filter = ['activo']
    list_editable = ['activo', 'descuento']
    search_fields = ['codigo']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'titulo', 'created']
    list_filter = ['rating']
    search_fields = ['titulo', 'comentario']


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'user', 'leida', 'created']
    list_filter = ['leida']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo', 'order']
    list_editable = ['activo', 'order']
