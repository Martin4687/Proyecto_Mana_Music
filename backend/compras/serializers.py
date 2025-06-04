from rest_framework import serializers
from .models import Compra, DetalleCompra
from proveedor.serializers import ProveedorSerializer
from proveedor.models import Proveedor

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ['id_producto', 'cantidad', 'precio_unitario', 'subtotal']

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    id_proveedor = ProveedorSerializer(read_only=True)
    proveedor_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        source='id_proveedor',
        queryset=Proveedor.objects.all()
    )

    class Meta:
        model = Compra
        fields = ['id', 'fecha_compra', 'total', 'proveedor_id', 'id_proveedor', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        compra = Compra.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetalleCompra.objects.create(id_compra=compra, **detalle_data)
        
        return compra

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        
        # Actualizar compra
        instance.total = validated_data.get('total', instance.total)
        instance.id_proveedor = validated_data.get('id_proveedor', instance.id_proveedor)
        instance.save()
        
        # Actualizar detalles si existen
        if detalles_data is not None:
            instance.detalles.all().delete()
            for detalle_data in detalles_data:
                DetalleCompra.objects.create(id_compra=instance, **detalle_data)
        
        return instance

class CompraDetalleSerializer(serializers.ModelSerializer):
    id_proveedor = ProveedorSerializer(read_only=True)
    proveedor_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        source='id_proveedor',
        queryset=Compra.id_proveedor.field.related_model.objects.all()
    )

    class Meta:
        model = Compra
        fields = ['id', 'fecha_compra', 'total', 'id_proveedor', 'proveedor_id']
    
    def create(self, validated_data):
        return Compra.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.total = validated_data.get('total', instance.total)
        instance.id_proveedor = validated_data.get('id_proveedor', instance.id_proveedor)
        instance.save()
        return instance