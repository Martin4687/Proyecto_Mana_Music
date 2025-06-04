from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'email', 'fecha_registro')
    search_fields = ('nombre', 'contacto', 'email')
    list_filter = ('fecha_registro',)
    date_hierarchy = 'fecha_registro'