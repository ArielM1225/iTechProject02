# Generated by Django 4.2.5 on 2024-10-09 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0004_producto_cantidad_droga_producto_forma_farmaceutica_and_more'),
        ('Comunidad', '0013_alter_localidad_options'),
        ('Movimientos', '0008_historialmovimiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialmovimiento',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='historialmovimiento',
            name='id',
        ),
        migrations.RemoveField(
            model_name='historialmovimiento',
            name='producto',
        ),
        migrations.AddField(
            model_name='historialmovimiento',
            name='ajuste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Movimientos.ajustestock'),
        ),
        migrations.AddField(
            model_name='historialmovimiento',
            name='entrada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Movimientos.entrada'),
        ),
        migrations.AddField(
            model_name='historialmovimiento',
            name='id_historial',
            field=models.AutoField(default=1, primary_key=True, serialize=False, verbose_name='Código de movimiento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialmovimiento',
            name='salida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Movimientos.salida'),
        ),
        migrations.AlterField(
            model_name='ajusteproducto',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Productos.producto'),
        ),
        migrations.AlterField(
            model_name='ajusteproducto',
            name='tipo_mov',
            field=models.CharField(choices=[('ajuste de entrada', 'Ajuste de entrada'), ('ajuste de salida', 'Ajuste de salida')], max_length=20, verbose_name='Tipo de Movimiento'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='id_Proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Comunidad.proveedor', verbose_name='Proveedor'),
        ),
        migrations.AlterField(
            model_name='entradaproducto',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Productos.producto'),
        ),
        migrations.AlterField(
            model_name='historialmovimiento',
            name='tipo_movimiento',
            field=models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida'), ('ajuste de entrada', 'Ajuste de entrada'), ('ajuste de salida', 'Ajuste de salida')], max_length=20),
        ),
        migrations.AlterField(
            model_name='salida',
            name='id_Paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Comunidad.paciente', verbose_name='Nombre del paciente'),
        ),
        migrations.AlterField(
            model_name='salidaproducto',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Productos.producto'),
        ),
        migrations.CreateModel(
            name='HistorialProductos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('historial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movimientos.historialmovimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Productos.producto')),
            ],
            options={
                'verbose_name': 'Detalle de productos',
                'verbose_name_plural': 'Detalle de productos',
            },
        ),
    ]