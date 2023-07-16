from django.db import models
from user.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class OrderStatus(models.TextChoices):
        PENDING = ('PE', 'Pendiente')
        PROCESSING = ('PR', 'Procesando')
        SHIPPED = ('SH', 'Enviado')
        DELIVERED = ('DE', 'Entregado')
        CANCELLED = ('CA', 'Cancelado')

    status = models.CharField(
        'Estado',
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    class ShipmentMethod(models.TextChoices):
        PICKUP = ('P', "Retirar en tienda")
        STANDARD = ('S', 'Estándar')
        EXPRESS = ('E', 'Express')

    shipment_method = models.CharField(
        'Método de envío', max_length=1,
        choices=ShipmentMethod.choices,
        default=ShipmentMethod.PICKUP
    )

    """
    esto lo pongo aqui por si se utiliza en otras partes de la app
    habria que analizar de ponerlo en un modelo aparte asi un operador tiene la posibilidad de modificar envios
    y precios pero como no se menciono requisito lo hice de la forma mas simple que se me ha ocurrido
    """
    SHIPMENT_METHODS_PRICES = {
        ShipmentMethod.PICKUP: 0,
        ShipmentMethod.STANDARD: 5,
        ShipmentMethod.EXPRESS: 10,
    }

    total_price = models.DecimalField('Costo de envío', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"#{self.order.id} - {self.product.name} x{self.quantity}"