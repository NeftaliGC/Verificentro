"""
URL configuration for verificentroSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from modules.inicio import views
from modules.modulo_regulaciones import views as regulaciones_views


urlpatterns = [

    # Rutas principales
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),

    # Normativas
    path('nueva-normativa/', regulaciones_views.nueva_normativa, name='nueva_normativa'),
    path('editar-normativa/<int:pk>/', regulaciones_views.editar_normativa, name='editar_normativa'),
    path('eliminar-normativa/<int:pk>/', regulaciones_views.eliminar_normativa, name='eliminar_normativa'),
    path('listar_normativas/', regulaciones_views.listar_normativas, name='listar_normativas'),

    # Reportes
    path('reportes/', regulaciones_views.reportes, name='reportes'),
    path('reporte_aprobados/', regulaciones_views.reporte_vehiculos_aprobados, name='reporte_aprobados'),
    path('reporte_rechazados/', regulaciones_views.reporte_vehiculos_rechazados, name='reporte_rechazados'),
    path('reporte-multas-generadas/', regulaciones_views.reporte_multas_generadas, name='reporte_multas_generadas'),

    # Verificación vehicular
    path('verificacion/', regulaciones_views.verificacion_vehicular, name='verificacion_vehicular'),

]
