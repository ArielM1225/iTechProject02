# Generated by Django 4.2.5 on 2024-10-24 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0016_alter_contacto_calle_alter_contacto_código_postal_and_more'),
        ('Productos', '0008_droga_alter_producto_unique_together_drogaproducto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccionFarma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Acción Farmacológica',
                'verbose_name_plural': 'Acción Farmacológica',
            },
        ),
        migrations.AlterModelOptions(
            name='drogaproducto',
            options={'verbose_name': 'Droga contenida', 'verbose_name_plural': 'Drogas contenidas'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterField(
            model_name='drogaproducto',
            name='id_droga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Productos.droga', verbose_name='Droga'),
        ),
        migrations.AlterField(
            model_name='drogaproducto',
            name='id_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Productos.producto'),
        ),
        migrations.AlterField(
            model_name='drogaproducto',
            name='medida',
            field=models.CharField(choices=[('gramos', 'G'), ('miligramos', 'mg'), ('litros', 'L'), ('mililitros', 'ml')], max_length=20, verbose_name='Unidad de medida'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='id_Laboratorio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Comunidad.laboratorio', verbose_name='Laboratorio'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='presentacion',
            field=models.IntegerField(blank=True, help_text='Ejemplo: Caja x 30', null=True, verbose_name='Presentación'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='accion_farma',
            field=models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.PROTECT, to='Productos.accionfarma', verbose_name='Acción Farmacológica'),
        ),
    ]
