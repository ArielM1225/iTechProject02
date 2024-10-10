# Generated by Django 4.2.5 on 2024-10-02 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0003_producto_stock'),
        ('Movimientos', '0007_alter_ajustestock_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_movimiento', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida'), ('ajuste', 'Ajuste de Stock')], max_length=10)),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha_movimiento', models.DateTimeField(auto_now_add=True)),
                ('motivo', models.CharField(blank=True, max_length=150, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Productos.producto')),
            ],
        ),
    ]