from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    serie = models.CharField(max_length=30)
    marca = models.CharField(max_length=50)
    submarca = models.CharField(max_length=50)
    modelo = models.PositiveIntegerField()
    dueño = models.CharField(max_length=100)  
    correo = models.EmailField()

    def __str__(self):
        return f"{self.placa} - {self.dueño}"


class Cita(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=100)
    verificentro = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Cita para {self.vehiculo.placa} en {self.municipio} el {self.fecha} a las {self.hora}"
