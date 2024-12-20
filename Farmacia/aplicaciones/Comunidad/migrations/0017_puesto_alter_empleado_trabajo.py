# Generated by Django 4.2.4 on 2024-10-28 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Comunidad', '0016_alter_contacto_calle_alter_contacto_código_postal_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id_Puesto', models.AutoField(primary_key=True, serialize=False)),
                ('puesto_Nombre', models.CharField(blank=None, max_length=50, null=None, verbose_name='Puesto')),
                ('producto_Psiquiatrico', models.BooleanField(default=False, verbose_name='Acceso a productos psiquiátricos')),
            ],
        ),
        migrations.AlterField(
            model_name='empleado',
            name='trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Comunidad.puesto', verbose_name='Puesto'),
        ),
    ]
