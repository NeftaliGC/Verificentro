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
from django.urls import path, include
from modules.inicio import views as inicio_views
from modules.panel_empleado import views as empleado_views
from modules.modulo_regulaciones import views as regulaciones_views

urlpatterns = [
    # ======================= Rutas principales =======================
    path('admin/', admin.site.urls),
    path('', inicio_views.home, name='home'),

    # ------- Usuarios --------
    path('login/', inicio_views.login_usuario, name='login'),  # Login para usuarios
    path('registro/', inicio_views.registro, name='registro'),
    path('registrar-usuario/', inicio_views.registrar_usuario, name='registrar_usuario'),
    path('panel-usuario/', inicio_views.panel_usuario, name='panel_usuario'),
    path('logout/', inicio_views.logout, name='logout'),
    # ------- Empleados --------
    path('panel-empleado/', empleado_views.panel_empleado, name='panel_empleado'),
    path('login_empleado/', empleado_views.login_empleado, name='login_empleado'),  # Login para usuarios
    path('logout_empleado/', empleado_views.logout_empleado, name='logout_empleado'),



    # ======================= Modulo de regulaciones =======================  
    #path('panel-regulaciones/', regulaciones_views.panel_regulaciones, name='panel_regulaciones'),

    # Normativas
    #path('nueva-normativa/', regulaciones_views.nueva_normativa, name='nueva_normativa'),
    #path('editar-normativa/<int:pk>/', regulaciones_views.editar_normativa, name='editar_normativa'),
    #path('eliminar-normativa/<int:pk>/', regulaciones_views.eliminar_normativa, name='eliminar_normativa'),
    #path('listar_normativas/', regulaciones_views.listar_normativas, name='listar_normativas'),

    # Reportes
    #path('reportes/', regulaciones_views.reportes, name='reportes'),
    #path('reporte_aprobados/', regulaciones_views.reporte_vehiculos_aprobados, name='reporte_aprobados'),
    #path('reporte_rechazados/', regulaciones_views.reporte_vehiculos_rechazados, name='reporte_rechazados'),
    #path('reporte-multas-generadas/', regulaciones_views.reporte_multas_generadas, name='reporte_multas_generadas'),

    # Verificación vehicular
    #path('verificacion/', regulaciones_views.verificacion_vehicular, name='verificacion_vehicular'),

    # Pagos / Finanzas
    path('pagos/', include('modules.modulo_pagos.urls'))

    # ======================= Modulo de gobierno =======================
]
