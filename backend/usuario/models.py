# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser



class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    ci = models.CharField(max_length=20, unique=True)
    #rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, db_column='id_rol')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"
    
    class Meta:
        db_table = 'usuario_persona'

class Usuario(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='id_persona')
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'usuario_usuario'

