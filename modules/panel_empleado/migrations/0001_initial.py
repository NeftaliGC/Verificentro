# Generated by Django 5.2 on 2025-05-06 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('correo_personal', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=20)),
                ('contrasena', models.CharField(max_length=128)),
                ('rol', models.CharField(max_length=50)),
                ('numero_cuenta', models.CharField(max_length=30)),
            ],
        ),
    ]
