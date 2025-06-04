from django.contrib import admin
from .models import Venta

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_venta', 'cliente_nombre', 'total']
    list_filter = ['fecha_venta', 'id_cliente']
    search_fields = ['id_cliente__nombre', 'id_cliente__email', 'total']
    readonly_fields = ['fecha_venta']
    ordering = ['-fecha_venta']
    
    def cliente_nombre(self, obj):
        return obj.id_cliente.nombre
    cliente_nombre.short_description = 'Cliente'