from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CompraViewSet

router = DefaultRouter()
router.register(r'compras', CompraViewSet, basename='compra')

urlpatterns = router.urls