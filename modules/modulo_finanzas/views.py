from django.shortcuts import render
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from .serializers import PagoListSerializer, MultaListSerializer
from modules.inicio.models import Pago, Cita, Usuario, Multa, Vehiculo
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Sum

# Create your views here.

class ReporteFinanciero(APIView):
    def get(self, request):
        # Suponiendo que quieres un reporte mensual
        fecha_inicio = datetime.now().replace(day=1)  # Primer día del mes actual
        fecha_fin = datetime.now()  # Fecha actual

        # Cálculo de pagos totales
        pagos_totales = Pago.objects.filter(fecha_pago__range=[fecha_inicio, fecha_fin]).aggregate(total_pago=Sum('monto'))

        # Cálculo de multas totales
        multas_totales = Multa.objects.filter(fecha_imposicion__range=[fecha_inicio, fecha_fin]).aggregate(total_multa=Sum('monto'))

        reporte = {
            "total_pagos": pagos_totales['total_pago'] or 0,
            "total_multas": multas_totales['total_multa'] or 0,
            "balance": (pagos_totales['total_pago'] or 0) - (multas_totales['total_multa'] or 0),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        return Response(reporte)
    

# Filtro para los pagos
class PagoFilter(django_filters.FilterSet):
    placa = django_filters.CharFilter(field_name="id_cita__placa", lookup_expr='exact')
    monto_min = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')  # Filtro para monto mínimo
    monto_max = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')  # Filtro para monto máximo
    fecha_pago_min = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='gte')  # Filtro para fecha mínima
    fecha_pago_max = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='lte')  # Filtro para fecha máxima

    class Meta:
        model = Pago
        fields = ['placa', 'monto_min', 'monto_max', 'fecha_pago_min', 'fecha_pago_max']

# ViewSet para el modelo Pago
class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PagoFilter
    ordering_fields = ['fecha_pago', 'monto']  # Permite ordenar por fecha de pago o monto

    # Método para actualizar el estado y la fecha del pago
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Verificar que el estado no sea modificado si ya está confirmado
        if instance.estado == "Aprobado":
            return Response({"detail": "No se puede modificar el estado de un pago confirmado."}, status=400)
        
        # Si se va a modificar el estado o fecha, actualizamos la fecha del pago
        if "estado" in request.data and request.data["estado"] == "Aprobado":
            request.data["fecha_pago"] = datetime.now()  # Establecemos la fecha de pago actual

        return super().update(request, *args, **kwargs)
    

# Filtro para las multas
class MultaFilter(django_filters.FilterSet):
    placa = django_filters.CharFilter(field_name="placa", lookup_expr='exact')
    monto_min = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')  # Filtro para monto mínimo
    monto_max = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')  # Filtro para monto máximo
    fecha_imposicion_min = django_filters.DateFilter(field_name='fecha_imposicion', lookup_expr='gte')  # Filtro para fecha mínima
    fecha_imposicion_max = django_filters.DateFilter(field_name='fecha_imposicion', lookup_expr='lte')  # Filtro para fecha máxima

    class Meta:
        model = Multa
        fields = ['placa', 'monto_min', 'monto_max', 'fecha_imposicion_min', 'fecha_imposicion_max']

# ViewSet para el modelo Multa
class MultaViewSet(viewsets.ModelViewSet):
    queryset = Multa.objects.all()
    serializer_class = MultaListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = MultaFilter
    ordering_fields = ['fecha_imposicion', 'monto']  # Permite ordenar por fecha de imposición o monto

    # Método para actualizar el estado de la multa
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Verificar que el estado no sea modificado si ya está pagada
        if instance.estado == "Pagada":
            return Response({"detail": "No se puede modificar el estado de una multa pagada."}, status=400)

        return super().update(request, *args, **kwargs)
    

