from django.db import models
from aplicaciones.Movimientos.models import Entrada, EntradaProducto
from aplicaciones.Movimientos.models import Salida, SalidaProducto
from django.core.validators import MinValueValidator

class Producto (models.Model):
    
    FORMA_FARMA_CHOICES=(
    ('1', 'Comprimidos'),
    ('2', 'Cápsulas'),
    ('3', 'Grageas'),
    ('4', 'Jarabe'),
    ('5', 'Suspensión'),
    ('6', 'Emulsión'),
    ('7', 'Polvos'),
    ('8', 'Ungüento'),
    ('9', 'Crema'),
    ('10', 'Gel'),
    ('11', 'Pomada'),
    ('12', 'Inhalador'),
    ('13', 'Aerosol'),
    ('14', 'Solución'),
    ('15', 'Gotas'),
    ('16', 'Parche transdérmico'),
    ('17', 'Supositorios'),
    ('18', 'Óvulos'),
    ('19', 'Ampollas'),
    ('20', 'Viales'),
    ('21', 'Implantes'),
    ('22', 'Pastillas'),
    ('23', 'Sublinguales'),
    ('24', 'Tabletas masticables'),
    ('25', 'Enemas'),
    ('26', 'Granulados'),
    ('27', 'Espuma'),
    )
    
    tipo_choice = (
        ('venta libre', 'Venta Libre'),
        ('bajo receta', 'Bajo Receta'),
        ('bajo receta duplicada', 'Bajo receta duplicado-Lista IV'),
    )
    
    id_producto= models.AutoField(primary_key=True)
    nombre_Comercial=models.CharField ('Nombre',max_length=50)
    id_Laboratorio = models.ForeignKey('Comunidad.Laboratorio', on_delete=models.PROTECT, verbose_name= 'Laboratorio', blank=True, null=True)
    principio_activo=models.ManyToManyField ('Droga', through='DrogaProducto')
    forma_farmaceutica = models.CharField(
        max_length=100,
        help_text="Ejemplo: comprimido, jarabe, inyectable",
        null=True, verbose_name= 'Forma farmacéutica',
        choices=FORMA_FARMA_CHOICES
    )
    presentacion = models.IntegerField(
        help_text="Ejemplo: Caja x 30",
        null=True, blank=True, verbose_name='Presentación'
    )
    tipo_Producto=models.CharField(choices=tipo_choice, max_length=45, verbose_name='Tipo de medicamento')
    accion_farma=models.ForeignKey ('AccionFarma', max_length=100, on_delete=models.PROTECT, verbose_name='Acción Farmacológica', blank=True, null=True)
    stock = models.PositiveBigIntegerField(default=0) # Campo de stock, no permite valores negativos
    
    class Meta:
        verbose_name= 'Producto'
        verbose_name_plural='Productos'
    
    def __str__(self):
        return self.nombre_Comercial
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.stock = 0
        super().save(*args, **kwargs)
        
        
class Droga(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
class DrogaProducto(models.Model):
    
    MEDIDA_CHOICES = (
        ('gramos', 'G'),
        ('miligramos', 'mg'),
        ('litros', 'L'),
        ('mililitros', 'ml'),
    )
    
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=False, null=False)
    id_droga = models.ForeignKey(Droga, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Droga')
    cantidad = models.PositiveIntegerField()
    medida = models.CharField('Unidad de medida', max_length=20, choices=MEDIDA_CHOICES)
    
    def __str__(self):
        return f"{self.cantidad} de {self.id_droga} en {self.id_producto}"
    
    class Meta:
        verbose_name= 'Droga contenida'
        verbose_name_plural= 'Drogas contenidas'
        

class AccionFarma(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name= 'Acción Farmacológica'
        verbose_name_plural= 'Acción Farmacológica'
