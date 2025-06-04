"""
URL configuration for mana_music project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
#from django.views.generic.base import LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from proveedor.views import ProveedorViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', LoginView.as_view(), name='login'),
    path('api/', include('usuario.urls')),
    path('api/', include('productos.urls')),
    re_path(r'^$', RedirectView.as_view(url='/api/')),  # Redirige la raíz a /api/
    path('api/proveedores/', include('proveedor.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('compras.urls')),
    path('api/', include('ventas.urls')),
]
