from django.db import models
from aplicaciones.Movimientos.models import Entrada, EntradaProducto
from aplicaciones.Movimientos.models import Salida, SalidaProducto
from django.core.validators import MinValueValidator

class Producto (models.Model):
    UNIDAD_PESO_CHOICES = (
        ('mcg', 'Microgramo(s) (mcg)'),
        ('mg', 'Miligramo(s) (mg)'),
        ('g', 'Gramo(s) (g)'),
        ('ml','Mililitro(s) (ml)'),
        ('l','Litro(s) (l)'),
    )
    
    ACCION_FARMA_CHOICES= ( 
    ('1', 'Agente anabólico'),
    ('2', 'Analgésico'),
    ('3', 'Ansiolítico'),
    ('4', 'Antiácido'),
    ('5', 'Antianginoso'),
    ('6', 'Antibiótico'),
    ('7', 'Anticoagulante'),
    ('8', 'Anticolinérgico'),
    ('9', 'Anticolinesterásico'),
    ('10', 'Anticonvulsivo'),
    ('11', 'Antidiarreico'),
    ('12', 'Antidepresivo'),
    ('13', 'Antiemético'),
    ('14', 'Antiepiléptico'),
    ('15', 'Antiespasmódico'),
    ('16', 'Antiestamínico H2'),
    ('17', 'Antifúngico'),
    ('18', 'Antigotoso'),
    ('19', 'Antihipertensivo'),
    ('20', 'Antihistamínico'),
    ('21', 'Antiinflamatorio'),
    ('22', 'Antimicótico'),
    ('23', 'Antimalárico'),
    ('24', 'Antimigrañoso'),
    ('25', 'Antineoplásico'),
    ('26', 'Antinauseoso'),
    ('27', 'Antiparasitario'),
    ('28', 'Antipirético'),
    ('29', 'Antiplaquetario'),
    ('30', 'Antipsicótico'),
    ('31', 'Antiprotozoario'),
    ('32', 'Antiséptico'),
    ('33', 'Antiparkinsoniano'),
    ('34', 'Antitusígeno'),
    ('35', 'Antiviral'),
    ('36', 'Broncodilatador'),
    ('37', 'Cardiotónico'),
    ('38', 'Citotóxico'),
    ('39', 'Corticoide'),
    ('40', 'Descongestionante'),
    ('41', 'Diurético'),
    ('42', 'Estimulante'),
    ('43', 'Expectorante'),
    ('44', 'Hipnótico'),
    ('45', 'Hipocolesterolemiante'),
    ('46', 'Hipoglucemiante'),
    ('47', 'Hipoglucemiante oral'),
    ('48', 'Immunoestimulante'),
    ('49', 'Immunosupresor'),
    ('50', 'Laxante'),
    ('51', 'Mucolítico'),
    ('52', 'Parasimpaticomimético'),
    ('53', 'Relajante muscular'),
    ('54', 'Sedante'),
    ('55', 'Simpaticomimético'),
    ('56', 'Trombolítico'),
    ('57', 'Vasoconstrictor'),
    ('58', 'Vasodilatador'),
    )
    
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
    id_Laboratorio = models.ForeignKey('Comunidad.Laboratorio', on_delete=models.PROTECT, verbose_name= 'Laboratorio')
    principio_activo=models.CharField ('Droga principal',max_length=50)
    cantidad_droga = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Cantidad de la droga activa",
        null=True, blank=True
    )
    principio_activo_secundario=models.CharField ('Droga secundaria',max_length=50, default='Ninguno')
    cantidad_droga_secundario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Cantidad de la droga activa",
        null=True, blank=True
    )
    unidad_medida = models.CharField(
        max_length=10,
        choices=UNIDAD_PESO_CHOICES,
        help_text="Seleccione la unidad de medida. Por ejemplo: Gramos, Litros", null= False, verbose_name= 'Unidad de medida', default='Ninguno')
    forma_farmaceutica = models.CharField(
        max_length=100,
        help_text="Ejemplo: comprimido, jarabe, inyectable",
        null=True, verbose_name= 'Forma farmacéutica',
        choices=FORMA_FARMA_CHOICES
    )
    presentacion = models.IntegerField(
        help_text="Ejemplo: 30 comprimidos",
        null=True, blank=True, verbose_name='Presentación'
    )
    tipo_Producto=models.CharField(choices=tipo_choice, max_length=45, verbose_name='Tipo de medicamento')
    accion_farma=models.CharField ('Acción Farmacológica', max_length=100, choices=ACCION_FARMA_CHOICES)
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
    

    

    
    


