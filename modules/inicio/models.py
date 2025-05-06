# app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Multa(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.TextField()
    estado = models.BooleanField()

    def __str__(self):
        return f"Multa {self.id} - {'Pagada' if self.estado else 'Pendiente'}"


# Modelo de Vehiculos
class Vehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    tipo_combustible = models.CharField(max_length=20)  # Gasolina, Diésel, Eléctrico, Híbrido
    usa_obd = models.BooleanField()
    co_medido = models.DecimalField(max_digits=6, decimal_places=2)
    nox_medido = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.placa


class Usuario(AbstractUser):
    id = models.CharField(primary_key=True, max_length=100)

    USERNAME_FIELD = 'email'  # Login con correo
    REQUIRED_FIELDS = ['username']  # Para superusuario
    
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email



# Modelo de Citas
class Cita(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Cancelada', 'Cancelada'),
    ]
    id = models.CharField(primary_key=True, max_length=100)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    placa = models.ForeignKey(Vehiculo, to_field='placa', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"Cita {self.id} - {self.estado}"


# Modelo de Normativas
class Normativa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_combustible = models.CharField(max_length=20)
    limite_co = models.DecimalField(max_digits=6, decimal_places=2)
    limite_nox = models.DecimalField(max_digits=6, decimal_places=2)
    usa_obd = models.BooleanField()
    frecuencia_meses = models.IntegerField()
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField()

    def __str__(self):
        return self.nombre


# Modelo de Verificaciones
class Verificacion(models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.ForeignKey(Vehiculo, to_field='placa', on_delete=models.CASCADE)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    fecha = models.DateField()
    co_emitido = models.DecimalField(max_digits=6, decimal_places=2)
    nox_emitido = models.DecimalField(max_digits=6, decimal_places=2)
    obd_funciona = models.BooleanField()
    normativa_aplicada = models.ForeignKey(Normativa, on_delete=models.CASCADE)
    aprobada = models.BooleanField()

    def __str__(self):
        return f"Verificación {self.id} - {'Aprobada' if self.aprobada else 'Rechazada'}"


# Modelo de Reportes
class Reporte(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    id_verificacion = models.ForeignKey(Verificacion, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField()
    contenido = models.TextField()

    def __str__(self):
        return f"Reporte {self.id}"
    

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
