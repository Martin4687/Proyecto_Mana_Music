from django.db import models
from proveedor.models import Proveedor
from productos.models import Productos

class Compra(models.Model):
    id_proveedor = models.ForeignKey('proveedor.Proveedor', on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    #id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras')

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f"Compra #{self.id} - {self.fecha_compra.strftime('%d/%m/%Y')}"
    pass
    
class DetalleCompra(models.Model):
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    id_compra = models.ForeignKey(
        Compra, 
        on_delete=models.CASCADE, 
        related_name='detalles'
    )
    id_producto = models.ForeignKey(
        Productos, 
        on_delete=models.CASCADE,
        related_name='detalles_compra'
    )

    class Meta:
        db_table = 'detallecompra'  # Para mapear a la tabla existente

    def __str__(self):
        return f"Detalle {self.id} - Compra {self.id_compra.id}"