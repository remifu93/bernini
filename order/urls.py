from django.urls import path, include
from .routes import router
from .views import OrderListAPIView, OrderRetrieveAPIView, OrderCreateAPIView


urlpatterns = [
    path('', include(router.urls)),
    # path('list/', OrderListAPIView.as_view(), name='order-list'),
    # path('<int:pk>/', OrderRetrieveAPIView.as_view(), name='order-detail'),
    # path('create/', OrderCreateAPIView.as_view(), name='order-create'),
]
