from django.urls import path
from . import views  # Importa las vistas de tu módulo

app_name = 'finanzas'  # Namespace para evitar conflictos

urlpatterns = [
    path('ingreso-placa/', views.IngresoPlacaView.as_view(), name='ingreso_placa'),
]