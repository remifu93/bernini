# swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# django-rest
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

# django
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q

# local apps
from base.paginations import LittlePagination

# this app
from .models import Product
from .serializers import ProductSerializer


# Swagger definicion de parametros
doc_search_param = openapi.Parameter(
    'search',
    openapi.IN_QUERY,
    description='Filter products list by search string',
    type=openapi.TYPE_STRING
)


"""
Cacheo en redis cada 1 hora el listado de productos.

No es la mejor forma de hacerlo ya que si se agregan productos en el intervalo el cliente no veria los cambios
hasta que se updatee el cache.

Habria que utilizar una forma mas avanzada de cacheo si ese fuera un problema
por ejemplo al agregar, updatear, etc un producto y eso se podria hacer desde el modelo o con signals

La cache limita el numero de requests asi que tener en cuenta por el trottle, por si veis que no funciona
"""
# @method_decorator(cache_page(60*60), name='dispatch')
class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    pagination_class = LittlePagination
    throttle_classes = [AnonRateThrottle, ]  # en el settings.py estan los rates

    # Agrego en la documentacion de la api el queryparam search
    @swagger_auto_schema(manual_parameters=[doc_search_param])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)

        # podria usar una libreria como django-filters pero como era muy simple lo hice asi
        search = self.request.GET.get("search")
        if search:
            queryset = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return queryset
