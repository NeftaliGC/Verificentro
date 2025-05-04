# app/models.py
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=128)  # Idealmente usar hash

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


