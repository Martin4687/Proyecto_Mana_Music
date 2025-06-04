from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaViewSet, EstadisticasView, ClienteListView
from . import views

router = DefaultRouter()
router.register(r'ventas', VentaViewSet, basename='venta')

urlpatterns = [
    path('', include(router.urls)),
    path('ventas/clientes/', ClienteListView.as_view(), name='cliente-list'),  # Ruta corregida
    path('ventas/estadisticas/', EstadisticasView.as_view(), name='estadisticas'),  # Ruta corregida
]
