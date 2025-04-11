from django.urls import path, include
from rest_framework import routers
from modules.modulo_pagos.views import PagoViewSet, MultaViewSet, FacturaViewSet

router = routers.DefaultRouter()
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'multas', MultaViewSet, basename='multa')
router.register(r'facturas', FacturaViewSet, basename='factura')

urlpatterns = [
    path('', include(router.urls)),
]
