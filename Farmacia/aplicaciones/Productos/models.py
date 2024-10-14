from django.db import models
from aplicaciones.Movimientos.models import Entrada, EntradaProducto
from aplicaciones.Movimientos.models import Salida, SalidaProducto
from django.core.validators import MinValueValidator



        



class Producto (models.Model):
    UNIDAD_PESO_CHOICES = (
        ('mcg', 'Microgramo(s) (mcg)'),
        ('mg', 'Miligramo(s) (mg)'),
        ('g', 'Gramo(s) (g)'),
    )
    
    tipo_choice = (
        ('venta libre', 'Venta Libre'),
        ('bajo receta', 'Bajo Receta'),
        ('bajo receta duplicada', 'Bajo receta duplicado-Lista IV'),
    )
    
    id_producto= models.AutoField(primary_key=True)
    nombre_Comercial=models.CharField ('Nombre',max_length=50)
    id_Laboratorio = models.ForeignKey('Comunidad.Laboratorio', on_delete=models.PROTECT, verbose_name= 'Laboratorio')
    principio_activo=models.CharField ('Droga',max_length=50)
    cantidad_droga = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Cantidad de la droga activa",
        null=True
    )
    unidad_medida = models.CharField(
        max_length=10,
        choices=UNIDAD_PESO_CHOICES,
        help_text="Seleccione la unidad de medida apropiada", null= True, verbose_name= 'Unidad de medida')
    forma_farmaceutica = models.CharField(
        max_length=100,
        help_text="Ejemplo: comprimido, jarabe, inyectable",
        null=True, verbose_name= 'Forma farmacéutica'
    )
    presentacion = models.CharField(
        max_length=200,
        help_text="Ejemplo: Caja x 30 comprimidos",
        null=True, verbose_name='Presentación'
    )
    tipo_Producto=models.CharField(choices=tipo_choice, max_length=45, verbose_name='Tipo de producto')
    accion_farma=models.CharField ('Acción',max_length=50)
    stock = models.PositiveBigIntegerField(default=0) # Campo de stock, no permite valores negativos
    
    class Meta:
        verbose_name= 'Producto'
        verbose_name_plural='Medicamentos'
        unique_together=('nombre_Comercial','principio_activo','presentacion')
    
    def __str__(self):
        return self.nombre_Comercial
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.stock = 0
        super().save(*args, **kwargs)
    

    

    
    


