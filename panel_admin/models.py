from django.db import models
from django.contrib.auth.models import User
from tienda.models import Product
from carrito.models import Order


class Pago(models.Model):
    METODOS = (
        ('credit_card', 'Tarjeta de Credito'),
        ('debit_card', 'Tarjeta de Debito'),
        ('pse', 'PSE - Transferencia Bancaria'),
        ('nequi', 'Nequi'),
        ('daviplata', 'Daviplata'),
        ('efectivo', 'Efectivo contra entrega'),
    )
    ESTADOS = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('refunded', 'Reembolsado'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=50, unique=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pending')
    referencia = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.order_id} - {self.get_metodo_pago_display()} - ${self.monto}"


class Boleta(models.Model):
    ESTADOS = (
        ('emitida', 'Emitida'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    )
    numero = models.CharField(max_length=20, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='boleta')
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    cliente_direccion = models.CharField(max_length=500)
    cliente_ciudad = models.CharField(max_length=200)
    cliente_documento = models.CharField(max_length=30, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='emitida')
    observaciones = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Boleta {self.numero}"

    def save(self, *args, **kwargs):
        if not self.numero:
            last = Boleta.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.numero = f"BOL-{num:06d}"
        super().save(*args, **kwargs)


class Factura(models.Model):
    ESTADOS = (
        ('emitida', 'Emitida'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    )
    numero = models.CharField(max_length=20, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='factura')
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    cliente_direccion = models.CharField(max_length=500)
    cliente_ciudad = models.CharField(max_length=200)
    cliente_nit = models.CharField(max_length=30)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='emitida')
    observaciones = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Factura {self.numero}"

    def save(self, *args, **kwargs):
        if not self.numero:
            last = Factura.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.numero = f"FAC-{num:06d}"
        super().save(*args, **kwargs)


class Cupon(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de descuento")
    activo = models.BooleanField(default=True)
    uso_maximo = models.PositiveIntegerField(default=100)
    uso_actual = models.PositiveIntegerField(default=0)
    minimo_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    expira = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.descuento}% off"

    @property
    def esta_disponible(self):
        return self.activo and self.uso_actual < self.uso_maximo


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)
    titulo = models.CharField(max_length=200)
    comentario = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}*.)"


class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.titulo


class Banner(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300, blank=True)
    imagen = models.ImageField(upload_to='banners/', blank=True, null=True)
    url_destino = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.titulo
