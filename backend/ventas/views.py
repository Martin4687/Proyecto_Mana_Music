from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Venta, Cliente
from .serializers import VentaSerializer, VentaCreateUpdateSerializer, ClienteForVentaSerializer
from cliente.models import Cliente
from cliente.serializers import ClienteSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.select_related('id_cliente').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VentaCreateUpdateSerializer
        return VentaSerializer
    
    def get_queryset(self):
        queryset = Venta.objects.select_related('id_cliente').all()
        
        # Filtros opcionales
        cliente_id = self.request.query_params.get('cliente_id', None)
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        search = self.request.query_params.get('search', None)
        
        if cliente_id:
            queryset = queryset.filter(id_cliente=cliente_id)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_venta__gte=fecha_desde)
        
        if fecha_hasta:
            queryset = queryset.filter(fecha_venta__lte=fecha_hasta)
        
        if search:
            queryset = queryset.filter(
                Q(id_cliente__nombre__icontains=search) |
                Q(id_cliente__email__icontains=search) |
                Q(total__icontains=search)
            )
        
        return queryset.order_by('-fecha_venta')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            venta = serializer.save()
            # Devolver la venta creada con todos los datos
            response_serializer = VentaSerializer(venta)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            venta = serializer.save()
            # Devolver la venta actualizada con todos los datos
            response_serializer = VentaSerializer(venta)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def clientes(self, request):
        """Endpoint para obtener lista de clientes para el selector"""
        clientes = Cliente.objects.all().order_by('nombre')
        serializer = ClienteForVentaSerializer(clientes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para obtener estadísticas básicas de ventas"""
        from django.db.models import Sum, Count, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # Estadísticas generales
        total_ventas = Venta.objects.aggregate(
            total_amount=Sum('total'),
            total_count=Count('id'),
            promedio=Avg('total')
        )
        
        # Ventas del mes actual
        hoy = timezone.now()
        inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ventas_mes = Venta.objects.filter(fecha_venta__gte=inicio_mes).aggregate(
            total_mes=Sum('total'),
            count_mes=Count('id')
        )
        
        return Response({
            'total_ventas': total_ventas['total_amount'] or 0,
            'cantidad_ventas': total_ventas['total_count'] or 0,
            'promedio_venta': total_ventas['promedio'] or 0,
            'ventas_mes': ventas_mes['total_mes'] or 0,
            'cantidad_ventas_mes': ventas_mes['count_mes'] or 0,
        })
    
# Agrega estas vistas si no existen
class VentaListCreate(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class VentaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class ClienteListView(generics.ListAPIView):
    queryset = Cliente.objects.all().order_by('nombre')
    serializer_class = ClienteForVentaSerializer

class EstadisticasView(generics.GenericAPIView):
    def get(self, request):
        # Lógica mejorada de estadísticas
        from django.db.models import Sum, Count, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # Estadísticas generales
        total_ventas = Venta.objects.aggregate(
            total_amount=Sum('total'),
            total_count=Count('id'),
            promedio=Avg('total')
        )
        
        # Ventas del mes actual
        hoy = timezone.now()
        inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ventas_mes = Venta.objects.filter(fecha_venta__gte=inicio_mes).aggregate(
            total_mes=Sum('total'),
            count_mes=Count('id')
        )
        
        return Response({
            'total_ventas': total_ventas['total_amount'] or 0,
            'cantidad_ventas': total_ventas['total_count'] or 0,
            'promedio_venta': total_ventas['promedio'] or 0,
            'ventas_mes': ventas_mes['total_mes'] or 0,
            'cantidad_ventas_mes': ventas_mes['count_mes'] or 0,
        }) 