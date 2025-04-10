# app/models.py
from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, primary_key=True)
    propietario = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    clase = models.CharField(max_length=50)
    combustible = models.CharField(max_length=50)
    cilindros = models.IntegerField()

class Usuario(models.Model):
    id_usuario = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=[('Cliente', 'Cliente'), ('Trabajador', 'Trabajador')])

class Cita(models.Model):
    id_cita = models.CharField(max_length=50, primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    placa = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Cancelada', 'Cancelada')])

class Trabajador(models.Model):
    id_trabajador = models.CharField(max_length=50, primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[('Técnico', 'Técnico'), ('Revisor', 'Revisor')])

class Pago(models.Model):
    id_pago = models.CharField(max_length=50, primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')])

class Regulacion(models.Model):
    id_regulacion = models.CharField(max_length=50, primary_key=True)
    metodo = models.CharField(max_length=100)
    limite_HO = models.IntegerField()
    limite_CO = models.IntegerField()
    limite_NO = models.IntegerField()
    limite_O2 = models.IntegerField()
    dilucion = models.IntegerField()
    factor_lambda = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio_verificacion = models.DateField()
    fecha_fin_verificacion = models.DateField()

class Resultado(models.Model):
    id_resultado = models.CharField(max_length=50, primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    HO = models.IntegerField()
    CO = models.IntegerField()
    NO = models.IntegerField()
    O2 = models.IntegerField()
    dilucion = models.IntegerField()
    factor_lambda = models.DecimalField(max_digits=5, decimal_places=2)
    resultado = models.CharField(max_length=20, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')])
    fecha = models.DateTimeField()

class Reporte(models.Model):
    id_reporte = models.CharField(max_length=50, primary_key=True)
    id_resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField()
    contenido = models.TextField()

class Multa(models.Model):
    id_multa = models.CharField(max_length=50, primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    placa = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255)
    fecha_imposicion = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Pagada', 'Pagada')])
