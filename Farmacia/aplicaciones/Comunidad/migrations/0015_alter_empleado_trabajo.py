# Generated by Django 4.2.5 on 2024-10-16 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0014_alter_contacto_localidad_alter_empleado_id_contacto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='trabajo',
            field=models.CharField(choices=[('auxiliar', 'Auxiliar'), ('administrativo', 'Administrativo'), ('farmacéutico', 'Farmacéutico'), ('médico', 'Médico')], max_length=20, verbose_name='Puesto'),
        ),
    ]
