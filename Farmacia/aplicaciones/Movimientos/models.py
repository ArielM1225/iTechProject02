from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
# from Productos.models import calcular_stock


class Entrada(models.Model):
    id_Entrada = models.AutoField(primary_key=True, verbose_name='Código de movimiento')
    productos = models.ManyToManyField('Productos.Producto', through='EntradaProducto')
    Remito = models.ImageField('Remito', null=True, blank=True)
    id_Proveedor = models.ForeignKey('Comunidad.Proveedor', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Proveedor')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    def __str__(self):
        return f'Número de entrada: {self.id_Entrada}'

class EntradaProducto(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey('Productos.Producto', on_delete=models.PROTECT, blank=True, null=True)
    fecha_Caducidad = models.DateField('Fecha de caducidad')
    cantidad = models.PositiveIntegerField()

@receiver(post_save, sender=EntradaProducto)
def adjust_stock(sender, created, instance, **kwargs):
    if created:
        # Aumentar el stock cuando se crea una nueva EntradaProducto
        if instance.producto is not None:
            ordered_qty = instance.cantidad
            
            # Aumenta el stock del producto
            instance.producto.stock += ordered_qty
            instance.producto.save()
            
            historial, _ = HistorialMovimiento.objects.get_or_create(
                entrada=instance.entrada,
                tipo_movimiento='entrada',
                defaults={'fecha_movimiento': instance.entrada.created_at}
            )
            
            # Crea el detalle del historial
            HistorialProductos.objects.create(
                historial=historial,
                producto=instance.producto,
                cantidad=instance.cantidad
            )

class Salida(models.Model):
    id_Salida = models.AutoField(primary_key=True, verbose_name='Código de movimiento')
    productos = models.ManyToManyField('Productos.Producto', through='SalidaProducto')
    recetas = models.CharField ('Receta',max_length=100)
    duplicado = models.ImageField('Duplicado', null=True, blank=True)
    id_Paciente = models.ForeignKey('Comunidad.Paciente', on_delete=models.PROTECT, verbose_name= 'Nombre del paciente')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    entregado = models.BooleanField('Entregado', default=False)


    def __str__(self):
        return f'Número de salida: {self.id_Salida}'

class SalidaProducto(models.Model):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey('Productos.Producto', on_delete=models.PROTECT, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
 
@receiver(post_save, sender=SalidaProducto)
def adjust_stock(sender, created, instance, **kwargs):
    if created:
        # Restar del stock solo si es una nueva SalidaProducto
        if instance.producto is not None:
            ordered_qty = instance.cantidad
            stocked_qty = instance.producto.stock

            # Verifica si hay suficiente stock antes de restar
            if stocked_qty >= ordered_qty:
                instance.producto.stock -= ordered_qty
                instance.producto.save()
                
                historial, _ = HistorialMovimiento.objects.get_or_create(
                salida=instance.salida,
                tipo_movimiento='salida',
                defaults={'fecha_movimiento': instance.entrada.created_at}
            )
            
            # Crea el detalle del historial
            HistorialProductos.objects.create(
                historial=historial,
                producto=instance.producto,
                cantidad=instance.cantidad
            )
                
        else:
                raise ValidationError(f'No hay suficiente stock disponible para el producto {instance.producto.nombre_Comercial}. Stock actual: {stocked_qty}')
            
            
            
class AjusteStock(models.Model):
    id_ajuste = models.AutoField(primary_key=True, verbose_name='Código de movimiento')
    motivo = models.CharField ('Motivo', max_length=150)
    productos = models.ManyToManyField('Productos.Producto', through='AjusteProducto')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')


    def __str__(self):
        return f'Número de ajuste: {self.id_ajuste}'
    
    class Meta:
        verbose_name = 'Ajuste de stock'
        verbose_name_plural = 'Ajustes de stock'

class AjusteProducto(models.Model):
    
    TIPO_MOV_CHOICES = (
        ('ajuste de entrada', 'Ajuste de entrada'),
        ('ajuste de salida', 'Ajuste de salida'),
    )
    
    tipo_mov = models.CharField('Tipo de Movimiento', max_length=20, choices=TIPO_MOV_CHOICES)
    ajuste = models.ForeignKey(AjusteStock, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey('Productos.Producto', on_delete=models.PROTECT, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f'Ajuste: {self.ajuste} - Producto: {self.producto}'
    

    
    
@receiver(post_save, sender=AjusteProducto)
def ajustar_stock(sender, created, instance, **kwargs):
    if created:
        producto = instance.producto
        cantidad = instance.cantidad

        if instance.tipo_mov == 'ajuste de entrada':
            producto.stock += cantidad
            tipo_movimiento = 'ajuste de entrada'
        elif instance.tipo_mov == 'ajuste de salida':
            if producto.stock < cantidad:
                raise ValidationError(f'Stock insuficiente para el producto {producto.nombre_Comercial}. Stock actual: {producto.stock}')
            producto.stock -= cantidad
            tipo_movimiento = 'ajuste de salida'

        producto.save()
        
        historial, _ = HistorialMovimiento.objects.get_or_create(
                ajuste=instance.ajuste,
                tipo_movimiento=tipo_movimiento,
                defaults={'fecha_movimiento': instance.entrada.created_at}
            )
            
            # Crea el detalle del historial
        HistorialProductos.objects.create(
                historial=historial,
                producto=instance.producto,
                cantidad=instance.cantidad
            )
        
        
class HistorialMovimiento(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste de entrada', 'Ajuste de entrada'),
        ('ajuste de salida', 'Ajuste de salida')
    )
    id_historial = models.AutoField(primary_key=True, verbose_name='Código de movimiento')
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=150, blank=True, null=True)  # Para registrar el motivo en caso de ajuste
    entrada = models.ForeignKey('Entrada', on_delete=models.SET_NULL, null=True, blank=True)
    salida = models.ForeignKey('Salida', on_delete=models.SET_NULL, null=True, blank=True)
    ajuste = models.ForeignKey('AjusteStock', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Movimiento: {self.tipo_movimiento}'
    
class HistorialProductos(models.Model):
        producto = models.ForeignKey('Productos.Producto', on_delete=models.PROTECT)
        cantidad = models.PositiveIntegerField()
        historial = models.ForeignKey(HistorialMovimiento, on_delete=models.CASCADE)
        class Meta:
            verbose_name = 'Detalle de productos'
            verbose_name_plural = 'Detalle de productos'
    
    
    
     
    #def save(self, *args, **kwargs):
        # Verificar si hay suficiente stock antes de realizar la salida
     #   if self.producto.stock < self.cantidad:
      #      raise ValidationError(f'No hay suficiente stock disponible para el producto {self.producto.nombre_Comercial}. Stock actual: {self.producto.stock}')
       # if not self.pk: # Si es una nueva salida
        #    self.producto.stock -= self.cantidad

        #super().save(*args, **kwargs)
        #self.producto.save()

  #  def delete(self, *args, **kwargs):
    # No modificar el stock al eliminar
   #     super().delete(*args, **kwargs)

# def calcular_stock(producto_id):
#     # Sumar todas las cantidades de entrada del producto
#     total_entradas = EntradaProducto.objects.filter(producto_id=producto_id).aggregate(total=Sum('cantidad'))['total'] or 0

#     # Sumar todas las cantidades de salida del producto
#     total_salidas = SalidaProducto.objects.filter(producto_id=producto_id).aggregate(total=Sum('cantidad'))['total'] or 0

#     # Calcular el stock actual
#     stock_actual = total_entradas - total_salidas

#     return stock_actual