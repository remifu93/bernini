"""
URL configuration for bernini project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required


# swagger schema
schema_view = get_schema_view(
   openapi.Info(
      title="Bernini API",
      default_version='v1',
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # documentacion generada con swagger
    path('', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),

    path('api/users/', include('user.urls')),
    path('api/products/', include('product.urls')),
    path('api/orders/', include('order.urls')),
]
