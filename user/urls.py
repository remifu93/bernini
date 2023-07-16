from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserCreateAPIView, TokenObtainView


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('token/', TokenObtainView.as_view(), name='token-get'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
