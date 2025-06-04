# urls.py de la aplicación manamusic

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'personas', PersonaViewSet)
router.register(r'usuarios', UsuarioViewSet)


urlpatterns = [
    path('api', include(router.urls)),
    
    # Rutas de autenticación
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]