from django.contrib import admin
from .models import Compra

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_compra', 'total', 'id_proveedor')
    list_filter = ('fecha_compra', 'id_proveedor')
    search_fields = ('id_proveedor__nombre',)
    date_hierarchy = 'fecha_compra'