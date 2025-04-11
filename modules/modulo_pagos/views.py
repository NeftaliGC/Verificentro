from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from modules.inicio.models import Pago, Cita, Vehiculo, Usuario, Multa
from modules.modulo_pagos.serializers import PagoSerializer, PagoListSerializer, MultaSerializer, MultaDetailSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()  # Podrías ajustar el queryset base según la lógica
    serializer_class = PagoSerializer

    # Acción para pagar el último pago pendiente por placa
    @action(detail=False, methods=['post'], url_path='pagar-por-placa')
    def pagar_por_placa(self, request):
        placa = request.data.get('placa')
        if not placa:
            return Response({"error": "Se requiere la placa"}, status=status.HTTP_400_BAD_REQUEST)
        # Buscar el último pago pendiente asociado a esta placa
        pago_pendiente = Pago.objects.filter(id_cita__placa=placa, estado="Pendiente").order_by('-fecha_pago').first()
        if not pago_pendiente:
            return Response({"error": "No se encontró pago pendiente para la placa indicada"}, status=status.HTTP_404_NOT_FOUND)
        # Actualización a pago aprobado
        pago_pendiente.estado = "Aprobado"
        # Aquí se establece la fecha de pago si es necesario: pago_pendiente.fecha_pago = timezone.now()
        pago_pendiente.save()
        return Response(PagoListSerializer(pago_pendiente).data, status=status.HTTP_200_OK)

    # Listado filtrado de pagos pendientes por placa
    @action(detail=False, methods=['get'], url_path='pendientes-por-placa')
    def pendientes_por_placa(self, request):
        placa = request.query_params.get('placa')
        if not placa:
            return Response({"error": "Se requiere la placa"}, status=status.HTTP_400_BAD_REQUEST)
        pagos = Pago.objects.filter(id_cita__placa=placa, estado="Pendiente")
        serializer = PagoListSerializer(pagos, many=True)
        return Response(serializer.data)


class MultaViewSet(viewsets.ModelViewSet):
    queryset = Multa.objects.all()
    serializer_class = MultaSerializer

    # Listado de multas pendientes por placa y usuario
    @action(detail=False, methods=['get'], url_path='pendientes-por-placa')
    def pendientes_por_placa(self, request):
        placa = request.query_params.get('placa')
        id_usuario = request.query_params.get('id_usuario')
        if not placa or not id_usuario:
            return Response({"error": "Se requieren placa e id_usuario"}, status=status.HTTP_400_BAD_REQUEST)
        multas = Multa.objects.filter(placa=placa, id_usuario=id_usuario, estado="Pendiente")
        serializer = MultaDetailSerializer(multas, many=True)
        return Response(serializer.data)

    # Acción para pagar una multa en específico
    @action(detail=True, methods=['post'], url_path='pagar')
    def pagar(self, request, pk=None):
        try:
            multa = self.get_object()
        except:
            return Response({"error": "Multa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        # Actualizar estado de la multa a "Pagada"
        multa.estado = "Pagada"
        # Actualizar fecha (si el modelo la tiene, p.ej., multa.fecha_pago = timezone.now())
        multa.save()
        return Response(MultaDetailSerializer(multa).data, status=status.HTTP_200_OK)
    

class FacturaViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'], url_path='factura-por-pago')
    def factura_por_pago(self, request):
        id_pago = request.query_params.get('id_pago')
        if not id_pago:
            return Response({"error": "Se requiere el id del pago"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pago = Pago.objects.get(id_pago=id_pago)
        except Pago.DoesNotExist:
            return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        if pago.estado != "Aprobado":
            return Response({"error": "La factura solo se puede generar para pagos aprobados"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Datos relevantes para la factura:
        factura_data = {
            "id_pago": pago.id_pago,
            "monto": pago.monto,
            "fecha_pago": pago.fecha_pago,
            "cita": {
                "id_cita": pago.id_cita.id_cita,
                "fecha": pago.id_cita.fecha,
                "estado": pago.id_cita.estado,
                "vehiculo": {
                    "placa": pago.id_cita.placa.placa,
                    "modelo": pago.id_cita.placa.modelo,
                    "tipo": pago.id_cita.placa.tipo,
                    # Agrega otros datos del vehículo según sea necesario
                },
                "usuario": {
                    "id_usuario": pago.id_cita.id_usuario.id_usuario,
                    "nombre": pago.id_cita.id_usuario.nombre,
                    "correo": pago.id_cita.id_usuario.correo,
                    # Agrega otros datos del usuario si es relevante
                }
            }
        }
        return Response(factura_data, status=status.HTTP_200_OK)
