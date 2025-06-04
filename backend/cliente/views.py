from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cliente, Persona, Rol
from .serializers import (
    ClienteSerializer, 
    ClienteCreateSerializer, 
    PersonaSerializer, 
    RolSerializer
)

class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all().select_related('id_persona', 'id_persona__id_rol')
    serializer_class = ClienteSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClienteCreateSerializer
        return ClienteSerializer
    
    def get_queryset(self):
        queryset = Cliente.objects.all().select_related('id_persona', 'id_persona__id_rol')
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                nombre__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        return queryset.order_by('-fecha_registro')

class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all().select_related('id_persona', 'id_persona__id_rol')
    serializer_class = ClienteSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Si se actualizan datos de persona
        if instance.id_persona and any(key in request.data for key in ['nombres', 'apellido_paterno', 'apellido_materno', 'ci']):
            persona = instance.id_persona
            if 'nombres' in request.data:
                persona.nombres = request.data['nombres']
            if 'apellido_paterno' in request.data:
                persona.apellido_paterno = request.data['apellido_paterno']
            if 'apellido_materno' in request.data:
                persona.apellido_materno = request.data['apellido_materno']
            if 'ci' in request.data:
                persona.ci = request.data['ci']
            persona.save()
        
        self.perform_update(serializer)
        return Response(serializer.data)

@api_view(['GET'])
def cliente_stats(request):
    """Estadísticas básicas de clientes"""
    total_clientes = Cliente.objects.count()
    clientes_con_persona = Cliente.objects.filter(id_persona__isnull=False).count()
    
    return Response({
        'total_clientes': total_clientes,
        'clientes_con_persona': clientes_con_persona,
        'clientes_sin_persona': total_clientes - clientes_con_persona
    })

@api_view(['GET'])
def roles_list(request):
    """Lista de roles disponibles"""
    roles = Rol.objects.all()
    serializer = RolSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_clientes(request):
    """Búsqueda de clientes"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])
    
    clientes = Cliente.objects.filter(
        nombre__icontains=query
    ).select_related('id_persona')[:10]
    
    results = []
    for cliente in clientes:
        results.append({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'email': cliente.email,
            'telefono': cliente.telefono,
            'persona_completa': str(cliente.id_persona) if cliente.id_persona else None
        })
    
    return Response(results)