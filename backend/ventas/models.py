from django.db import models
from django.utils import timezone
from cliente.models import Cliente

class Venta(models.Model):
    fecha_venta = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    
    class Meta:
        db_table = 'ventas_venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha_venta']
    
    def __str__(self):
        return f"Venta #{self.id} - {self.id_cliente.nombre} - ${self.total}"
    
    @property
    def cliente_nombre(self):
        return self.id_cliente.nombre
    
    @property
    def cliente_email(self):
        return self.id_cliente.email