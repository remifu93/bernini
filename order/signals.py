from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order


@receiver(pre_save, sender=Order)
def update_total_price(sender, instance, **kwargs):
    if not instance.total_price:
        instance.total_price = instance.SHIPMENT_METHODS_PRICES.get(instance.shipment_method, 0)
