# Generated by Django 4.2.4 on 2024-09-23 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0009_alter_laboratorio_id_contacto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacto',
            name='provincia',
        ),
    ]