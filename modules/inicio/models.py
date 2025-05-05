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


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Cancelada', 'Cancelada'),
    ]

    id = models.CharField(primary_key=True, max_length=100)
    id_usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE)
    placa = models.ForeignKey('Vehiculos', to_field='placa', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"Cita {self.id} - {self.estado}"


class Pago(models.Model):
    ESTADO_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    ]

    id = models.CharField(primary_key=True, max_length=100)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"


class Multa(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.TextField()
    estado = models.BooleanField()

    def __str__(self):
        return f"Multa {self.id} - {'Pagada' if self.estado else 'Pendiente'}"

