from django.db import models

# Create your models here.
# app/models.py
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    correo_personal = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=128)  # Idealmente usar hash
    rol = models.CharField(max_length=50)  # Ejemplo: 'administrador', 'empleado', etc.
    numero_cuenta = models.CharField(max_length=30)  # Puedes ajustar el tamaño según el formato

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} - {self.rol}"
