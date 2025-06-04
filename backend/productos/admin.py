from django.contrib import admin
from .models import Productos

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'fecha_registro')
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'descripcion')