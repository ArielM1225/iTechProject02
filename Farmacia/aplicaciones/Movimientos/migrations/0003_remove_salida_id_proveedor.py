# Generated by Django 4.2.5 on 2024-09-19 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movimientos', '0002_alter_entrada_id_entrada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salida',
            name='id_Proveedor',
        ),
    ]
