from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from base.permissions import ApiKeyPermission
from product.models import Product

from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer


# Class Based Views GENERICS
class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [ApiKeyPermission, IsAuthenticated, ]

    def get_queryset(self):
        authenticated_user = self.request.user

        if authenticated_user.is_staff or authenticated_user.is_superuser:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)

class OrderRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [ApiKeyPermission, IsAuthenticated, ]

    def get_queryset(self):
        authenticated_user = self.request.user
        if authenticated_user.is_staff or authenticated_user.is_superuser:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user.id)

class OrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shipment_method = serializer.validated_data['shipment_method']
        products = serializer.validated_data['products']

        order = Order.objects.create(
            user=self.request.user,
            shipment_method=shipment_method,
        )

        order_items = []
        products_total_price = 0
        for product in products:
            # se podria mejorar para no hacer una consulta por cada product de la order
            try:
                product_obj = Product.objects.get(pk=product['id'])
            except ObjectDoesNotExist:
                return Response({"error": f"el producto id {product['id']} no existe"})

            item = OrderItem(
                order=order,
                product=product_obj,
                quantity=product['quantity']
            )
            order_items.append(item)
            products_total_price += (product_obj.price * product['quantity'])

        order.total_price += products_total_price
        order.save()

        OrderItem.objects.bulk_create(order_items)

        return Response({"message": "orden creada con exito", "order": OrderDetailSerializer(order).data})


# Viewsets
class OrderViewSet(ModelViewSet):
    serializer_class = OrderListSerializer
    permission_classes = [ApiKeyPermission, IsAuthenticated, ]
    http_method_names = ['get', 'post']

    def get_queryset(self):

        # para evitar errores al generar automaticamente la doc con swagger
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()

        authenticated_user = self.request.user

        if authenticated_user.is_staff or authenticated_user.is_superuser:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = OrderListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shipment_method = serializer.validated_data['shipment_method']
        products = serializer.validated_data['products']

        order = Order.objects.create(
            user=self.request.user,
            shipment_method=shipment_method,
        )

        order_items = []
        products_total_price = 0
        for product in products:
            # se podria mejorar para no hacer una consulta por cada product de la order
            try:
                product_obj = Product.objects.get(pk=product['id'])
            except ObjectDoesNotExist:
                return Response({"error": f"el producto id {product['id']} no existe"})

            item = OrderItem(
                order=order,
                product=product_obj,
                quantity=product['quantity']
            )
            order_items.append(item)
            products_total_price += (product_obj.price * product['quantity'])

        order.total_price += products_total_price
        order.save()

        OrderItem.objects.bulk_create(order_items)

        return Response({"message": "orden creada con exito", "order": OrderDetailSerializer(order).data})
