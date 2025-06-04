from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Compra
from .serializers import CompraSerializer, CompraDetalleSerializer
from django_filters.rest_framework import DjangoFilterBackend

class CompraViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Compra.objects.prefetch_related('detalles').all()
    serializer_class = CompraSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id_proveedor']
    search_fields = ['id_proveedor__nombre']
    ordering_fields = ['fecha_compra', 'total']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return CompraDetalleSerializer
        return CompraSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)