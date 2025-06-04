from rest_framework import serializers
from .models import Venta
from cliente.models import Cliente

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='id_cliente.nombre', read_only=True)
    cliente_email = serializers.CharField(source='id_cliente.email', read_only=True)
    cliente_telefono = serializers.CharField(source='id_cliente.telefono', read_only=True)
    fecha_venta_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Venta
        fields = [
            'id', 
            'fecha_venta', 
            'fecha_venta_formatted',
            'total', 
            'id_cliente', 
            'cliente_nombre', 
            'cliente_email',
            'cliente_telefono'
        ]
        read_only_fields = ['id']
    
    def get_fecha_venta_formatted(self, obj):
        return obj.fecha_venta.strftime('%d/%m/%Y %H:%M')

class VentaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['fecha_venta', 'total', 'id_cliente']
    
    def validate_total(self, value):
        if value <= 0:
            raise serializers.ValidationError("El total debe ser mayor a 0")
        return value
    
    def validate_id_cliente(self, value):
        if not Cliente.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("El cliente seleccionado no existe")
        return value

class ClienteForVentaSerializer(serializers.ModelSerializer):
    """Serializer simple para obtener lista de clientes en el selector"""
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono']