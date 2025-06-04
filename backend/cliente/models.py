from django.db import models
from django.utils import timezone

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'cliente_rol'
    
    def __str__(self):
        return self.nombre_rol

class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    ci = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'cliente_persona'
    
    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nombre_usuario = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'cliente_cliente'
    
    def __str__(self):
        return self.nombre