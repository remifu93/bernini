from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass