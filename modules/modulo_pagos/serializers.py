# Pagos/serializers.py
from rest_framework import serializers
from modules.inicio.models import Usuario, Cita, Pago, Multa, Vehiculo  # Importamos el modelo de la aplicación 'inicio'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'  # Serializa todos los campos del modelo Usuario

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'  # Serializa todos los campos del modelo Cita
    
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'  # Serializa todos los campos del modelo Pago

class MultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multa
        fields = '__all__'  # Serializa todos los campos del modelo Multa

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'  # Serializa todos los campos del modelo Vehiculo

class MultaDetailSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(source='placa', read_only=True)

    class Meta:
        model = Multa
        fields = ['id_multa', 'vehiculo', 'monto', 'fecha_imposicion', 'estado']  # Campos a serializar en detalle de multa

class CitaListSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(source='id_usuario', read_only=True)
    vehiculo = VehiculoSerializer(source='placa', read_only=True)

    class Meta:
        model = Cita
        fields = ['id_cita', 'usuario', 'vehiculo', 'fecha', 'estado']  # Campos a serializar en lista de citas


class PagoListSerializer(serializers.ModelSerializer):
    cita = CitaListSerializer(source='id_cita', read_only=True)

    class Meta:
        model = Pago
        fields = ['id_pago', 'cita', 'monto', 'fecha_pago']  # Campos a serializar en lista de pagos

class CitaDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(source='id_usuario', read_only=True)
    vehiculo = VehiculoSerializer(source='placa', read_only=True)

    class Meta:
        model = Cita
        fields = ['id_cita', 'usuario', 'vehiculo', 'fecha', 'estado']  # Campos a serializar en detalle de cita

class PagoDetailSerializer(serializers.ModelSerializer):
    cita = CitaDetailSerializer(source='id_cita', read_only=True)

    class Meta:
        model = Pago
        fields = ['id_pago', 'cita', 'monto', 'fecha_pago']  # Campos a serializar en detalle de pago

class MultaListSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(source='placa', read_only=True)

    class Meta:
        model = Multa
        fields = ['id_multa', 'vehiculo', 'monto', 'fecha_imposicion', 'estado']  # Campos a serializar en lista de multas

class MultaDetailSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(source='placa', read_only=True)

    class Meta:
        model = Multa
        fields = ['id_multa', 'vehiculo', 'monto', 'fecha_imposicion', 'estado']  # Campos a serializar en detalle de multa

