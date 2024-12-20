# Generated by Django 4.2.4 on 2024-10-16 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0006_alter_producto_presentacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad_droga_secundario',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cantidad de la droga activa', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='producto',
            name='principio_activo_secundario',
            field=models.CharField(default='Ninguno', max_length=50, verbose_name='Droga secundaria'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='accion_farma',
            field=models.CharField(choices=[('1', 'Agente anabólico'), ('2', 'Analgésico'), ('3', 'Ansiolítico'), ('4', 'Antiácido'), ('5', 'Antianginoso'), ('6', 'Antibiótico'), ('7', 'Anticoagulante'), ('8', 'Anticolinérgico'), ('9', 'Anticolinesterásico'), ('10', 'Anticonvulsivo'), ('11', 'Antidiarreico'), ('12', 'Antidepresivo'), ('13', 'Antiemético'), ('14', 'Antiepiléptico'), ('15', 'Antiespasmódico'), ('16', 'Antiestamínico H2'), ('17', 'Antifúngico'), ('18', 'Antigotoso'), ('19', 'Antihipertensivo'), ('20', 'Antihistamínico'), ('21', 'Antiinflamatorio'), ('22', 'Antimicótico'), ('23', 'Antimalárico'), ('24', 'Antimigrañoso'), ('25', 'Antineoplásico'), ('26', 'Antinauseoso'), ('27', 'Antiparasitario'), ('28', 'Antipirético'), ('29', 'Antiplaquetario'), ('30', 'Antipsicótico'), ('31', 'Antiprotozoario'), ('32', 'Antiséptico'), ('33', 'Antiparkinsoniano'), ('34', 'Antitusígeno'), ('35', 'Antiviral'), ('36', 'Broncodilatador'), ('37', 'Cardiotónico'), ('38', 'Citotóxico'), ('39', 'Corticoide'), ('40', 'Descongestionante'), ('41', 'Diurético'), ('42', 'Estimulante'), ('43', 'Expectorante'), ('44', 'Hipnótico'), ('45', 'Hipocolesterolemiante'), ('46', 'Hipoglucemiante'), ('47', 'Hipoglucemiante oral'), ('48', 'Immunoestimulante'), ('49', 'Immunosupresor'), ('50', 'Laxante'), ('51', 'Mucolítico'), ('52', 'Parasimpaticomimético'), ('53', 'Relajante muscular'), ('54', 'Sedante'), ('55', 'Simpaticomimético'), ('56', 'Trombolítico'), ('57', 'Vasoconstrictor'), ('58', 'Vasodilatador')], max_length=100, verbose_name='Acción Farmacológica'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad_droga',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cantidad de la droga activa', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='forma_farmaceutica',
            field=models.CharField(choices=[('1', 'Comprimidos'), ('2', 'Cápsulas'), ('3', 'Grageas'), ('4', 'Jarabe'), ('5', 'Suspensión'), ('6', 'Emulsión'), ('7', 'Polvos'), ('8', 'Ungüento'), ('9', 'Crema'), ('10', 'Gel'), ('11', 'Pomada'), ('12', 'Inhalador'), ('13', 'Aerosol'), ('14', 'Solución'), ('15', 'Gotas'), ('16', 'Parche transdérmico'), ('17', 'Supositorios'), ('18', 'Óvulos'), ('19', 'Ampollas'), ('20', 'Viales'), ('21', 'Implantes'), ('22', 'Pastillas'), ('23', 'Sublinguales'), ('24', 'Tabletas masticables'), ('25', 'Enemas'), ('26', 'Granulados'), ('27', 'Espuma')], help_text='Ejemplo: comprimido, jarabe, inyectable', max_length=100, null=True, verbose_name='Forma farmacéutica'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='principio_activo',
            field=models.CharField(max_length=50, verbose_name='Droga principal'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='tipo_Producto',
            field=models.CharField(choices=[('venta libre', 'Venta Libre'), ('bajo receta', 'Bajo Receta'), ('bajo receta duplicada', 'Bajo receta duplicado-Lista IV')], max_length=45, verbose_name='Tipo de medicamento'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(choices=[('mcg', 'Microgramo(s) (mcg)'), ('mg', 'Miligramo(s) (mg)'), ('g', 'Gramo(s) (g)'), ('ml', 'Mililitro(s) (ml)'), ('l', 'Litro(s) (l)')], default='Ninguno', help_text='Seleccione la unidad de medida. Por ejemplo: Gramos, Litros', max_length=10, verbose_name='Unidad de medida'),
        ),
    ]
