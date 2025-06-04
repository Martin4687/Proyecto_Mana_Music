from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Productos
from .serializers import ProductosSerializer
from rest_framework.permissions import IsAuthenticated

class ProductosViewSet(viewsets.ModelViewSet):
    """
    API endpoint para productos.
    """
    queryset = Productos.objects.all().order_by('-fecha_registro')
    serializer_class = ProductosSerializer
    permission_classes = [permissions.IsAuthenticated]

