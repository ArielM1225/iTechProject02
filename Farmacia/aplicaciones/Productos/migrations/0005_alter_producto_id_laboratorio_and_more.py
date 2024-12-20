# Generated by Django 4.2.4 on 2024-10-15 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0014_alter_contacto_localidad_alter_empleado_id_contacto_and_more'),
        ('Productos', '0004_producto_cantidad_droga_producto_forma_farmaceutica_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id_Laboratorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Comunidad.laboratorio', verbose_name='Laboratorio'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='presentacion',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Ejemplo: 30 comprimidos', max_digits=10, null=True, verbose_name='Presentación'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(choices=[('mcg', 'Microgramo(s) (mcg)'), ('mg', 'Miligramo(s) (mg)'), ('g', 'Gramo(s) (g)'), ('ml', 'Mililitro(s) (ml)'), ('l', 'Litro(s) (l)')], help_text='Seleccione la unidad de medida apropiada', max_length=10, null=True, verbose_name='Unidad de medida'),
        ),
    ]
