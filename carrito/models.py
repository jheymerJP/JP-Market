from django.db import models
from django.conf import settings
from tienda.models import Product
import uuid


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity


ORDER_STATUS = (
    ('pending', 'Pendiente'),
    ('confirmed', 'Confirmado'),
    ('preparing', 'Preparando'),
    ('shipping', 'Enviado'),
    ('delivering', 'En reparto'),
    ('delivered', 'Entregado'),
    ('cancelled', 'Cancelado'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=10, choices=[('dni', 'DNI'), ('ruc', 'RUC'), ('ce', 'Carnet de Extranjeria')], default='dni')
    numero_documento = models.CharField(max_length=11, blank=True)
    tipo_comprobante = models.CharField(max_length=10, choices=[('boleta', 'Boleta'), ('factura', 'Factura')], default='boleta')
    razon_social = models.CharField(max_length=200, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Order {self.order_id}"

    @property
    def tracking_steps(self):
        steps = [
            ('pending', 'Pedido recibido', 'Tu pedido ha sido registrado'),
            ('confirmed', 'Confirmado', 'Tu pedido esta siendo verificado'),
            ('preparing', 'Preparando', 'Estamos preparando tu pedido'),
            ('shipping', 'Enviado', 'Tu pedido esta en camino'),
            ('delivering', 'En reparto', 'El repartidor va hacia ti'),
            ('delivered', 'Entregado', 'Tu pedido fue entregado'),
        ]
        current_idx = next(
            (i for i, (s, _, _) in enumerate(steps) if s == self.status), 0
        )
        return [
            {'key': s, 'title': t, 'desc': d, 'done': i <= current_idx, 'current': i == current_idx}
            for i, (s, t, d) in enumerate(steps)
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity
