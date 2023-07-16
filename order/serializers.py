from rest_framework import serializers
from .models import Order


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'user',
            'status',
            'shipment_method',
            'user',
        )

class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    quantity = serializers.IntegerField()

class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    products = serializers.SerializerMethodField()
    total_price = serializers.FloatField()

    class Meta:
        model = Order
        fields = [
            'id',
            'created_at',
            'user',
            'status',
            'shipment_method',
            'products',
            'total_price',
        ]

    def get_products(self, obj):
        queryset = obj.order_items.all()
        return OrderItemSerializer(queryset, many=True).data

class OrderItemCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderCreateSerializer(serializers.Serializer):
    shipment_method = serializers.CharField()
    products = OrderItemCreateSerializer(many=True)

    def validate_products(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Se requiere al menos 1 producto.")
        return value
