# Generated by Django 4.2.5 on 2024-10-02 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0012_rename_localidades_localidad_alter_empleado_trabajo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='localidad',
            options={'verbose_name': 'Localidad', 'verbose_name_plural': 'Localidades'},
        ),
    ]