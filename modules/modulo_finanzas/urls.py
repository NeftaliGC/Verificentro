from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PagoViewSet, MultaViewSet, ReporteFinanciero

router = DefaultRouter()
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'multas', MultaViewSet, basename='multa')

urlpatterns = [
    path('', include(router.urls)),
    path('reporte-financiero/', ReporteFinanciero.as_view(), name='reporte-financiero'),
]
