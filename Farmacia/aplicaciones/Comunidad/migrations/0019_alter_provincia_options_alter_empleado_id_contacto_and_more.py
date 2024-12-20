# Generated by Django 4.2.4 on 2024-11-13 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0018_alter_empleado_trabajo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provincia',
            options={'verbose_name': 'Provincia', 'verbose_name_plural': 'Provincias'},
        ),
        migrations.AlterField(
            model_name='empleado',
            name='id_Contacto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Comunidad.contacto', verbose_name='Información de contacto'),
        ),
        migrations.AlterField(
            model_name='localidad',
            name='Id_provincia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Comunidad.provincia', verbose_name='Provincia'),
        ),
        migrations.AlterField(
            model_name='puesto',
            name='producto_Psiquiatrico',
            field=models.BooleanField(default=False, verbose_name='Acceso Psiquiátrico'),
        ),
    ]
