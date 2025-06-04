from django.db import models

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'productos'
        db_table = 'producto'
        verbose_name = 'Productos'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre