# Generated by Django 4.2.5 on 2024-09-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0004_alter_contacto_departamento_alter_contacto_localidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='email',
            field=models.CharField(max_length=50, verbose_name='Correo electrónico'),
        ),
    ]
