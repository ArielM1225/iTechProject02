# Generated by Django 4.2.5 on 2024-10-02 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0010_remove_contacto_provincia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laboratorio',
            name='id_Contacto',
        ),
    ]
