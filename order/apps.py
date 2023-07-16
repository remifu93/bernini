from django.apps import AppConfig
from django.db.models.signals import pre_save



class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'

    def ready(self):
        from .models import Order
        from .signals import update_total_price
        pre_save.connect(update_total_price, sender=Order)