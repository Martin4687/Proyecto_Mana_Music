from django.contrib import admin
from .models import Cliente, Persona, Rol

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_rol']
    search_fields = ['nombre_rol']

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombres', 'apellido_paterno', 'apellido_materno', 'ci', 'id_rol', 'fecha_registro']
    list_filter = ['id_rol', 'fecha_registro']
    search_fields = ['nombres', 'apellido_paterno', 'ci']
    list_per_page = 20

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'email', 'telefono', 'id_persona', 'fecha_registro']
    list_filter = ['fecha_registro']
    search_fields = ['nombre', 'email', 'telefono']
    list_per_page = 20
    readonly_fields = ['fecha_registro']