from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Ciudadano(AbstractUser):  # Se corrige la herencia
    TIPOS_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('TI', 'Tarjeta de Identidad'),
    ]
    
    tipo_documento = models.CharField(
        max_length=2, 
        choices=TIPOS_DOCUMENTO,
        verbose_name="Tipo de Documento"
    )
    
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Documento"
    )
    
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    
    rfc = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="RFC con Homoclave",
        validators=[
            RegexValidator(
                regex='^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
                message='Formato de RFC inválido'
            )
        ]
    )
    
    curp = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CURP",
        validators=[
            RegexValidator(
                regex='^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$',
                message='Formato de CURP inválido'
            )
        ]
    )
    
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")
    verificado = models.BooleanField(default=False, verbose_name="Verificado")
    motivo_rechazo = models.TextField(blank=True, null=True, verbose_name="Motivo de Rechazo")

    def __str__(self):
        return f"{self.username} - {self.numero_documento}"

class SolicitudValidacion(models.Model):
    ESTADOS = (
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    )
    
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, verbose_name="Ciudadano")
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P', verbose_name="Estado")
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    fecha_resolucion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Resolución")
    respuesta_gobierno = models.JSONField(null=True, blank=True, verbose_name="Respuesta del Gobierno")

    def __str__(self):
        return f"Solicitud {self.id} - {self.ciudadano.username} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Solicitud de Validación"
        verbose_name_plural = "Solicitudes de Validación"

class HistorialCambios(models.Model):
    usuario = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, verbose_name="Usuario")
    registro_afectado = models.CharField(max_length=100, verbose_name="Registro Afectado")
    campo_modificado = models.CharField(max_length=100, verbose_name="Campo Modificado")
    valor_anterior = models.TextField(verbose_name="Valor Anterior")
    valor_nuevo = models.TextField(verbose_name="Valor Nuevo")
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Cambio")

    def __str__(self):
        return f"Cambio en {self.registro_afectado} por {self.usuario.username}"

    class Meta:
        verbose_name = "Historial de Cambio"
        verbose_name_plural = "Historial de Cambios"
