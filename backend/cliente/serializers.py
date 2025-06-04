from rest_framework import serializers
from .models import Cliente, Persona, Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class PersonaSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='id_rol.nombre_rol', read_only=True)
    
    class Meta:
        model = Persona
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='id_persona.nombres', read_only=True)
    persona_apellido = serializers.CharField(source='id_persona.apellido_paterno', read_only=True)
    persona_ci = serializers.CharField(source='id_persona.ci', read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.id_persona:
            representation['persona_completa'] = f"{instance.id_persona.nombres} {instance.id_persona.apellido_paterno}"
        return representation

class ClienteCreateSerializer(serializers.Serializer):
    # Datos del cliente
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=150)
    telefono = serializers.CharField(max_length=50, required=False, allow_blank=True)
    direccion = serializers.CharField(required=False, allow_blank=True)
    nombre_usuario = serializers.CharField(max_length=50, required=False, allow_blank=True)
    password = serializers.CharField(max_length=255, required=False, allow_blank=True)
    
    # Dados de la persona (opcional)
    nombres = serializers.CharField(max_length=100, required=False, allow_blank=True)
    apellido_paterno = serializers.CharField(max_length=100, required=False, allow_blank=True)
    apellido_materno = serializers.CharField(max_length=100, required=False, allow_blank=True)
    ci = serializers.CharField(max_length=20, required=False, allow_blank=True)
    id_rol = serializers.IntegerField(required=False)
    
    def validate_email(self, value):
        if Cliente.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un cliente con este email.")
        return value
    
    def validate_ci(self, value):
        if value and Persona.objects.filter(ci=value).exists():
            raise serializers.ValidationError("Ya existe una persona con este CI.")
        return value
    
    def create(self, validated_data):
        # Extraer datos de persona
        persona_data = {}
        if validated_data.get('nombres'):
            persona_data = {
                'nombres': validated_data.pop('nombres', ''),
                'apellido_paterno': validated_data.pop('apellido_paterno', ''),
                'apellido_materno': validated_data.pop('apellido_materno', ''),
                'ci': validated_data.pop('ci', ''),
                'id_rol_id': validated_data.pop('id_rol', None)
            }
        
        # Crear persona si se proporcionaron datos
        persona = None
        if persona_data and persona_data.get('nombres'):
            persona = Persona.objects.create(**persona_data)
        
        # Crear cliente
        cliente_data = validated_data
        if persona:
            cliente_data['id_persona'] = persona
            
        cliente = Cliente.objects.create(**cliente_data)
        return cliente