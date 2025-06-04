# backend/proveedores/serializers.py
from rest_framework import serializers
from .models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
        extra_kwargs = {
            'email': {'required': True},
            'fecha_registro': {'read_only': True}
        }