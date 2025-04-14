
from django.contrib import admin
from django.urls import path
from tasks import views 

urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/', admin.site.urls),
    path('verificacion/', views.verificacion, name='verificacion'), 
    path('citas/', views.citas, name='citas'),path('holograma-exento/', views.holograma_exento, name='holograma_exento'), path('constancia-d/', views.constancia_d, name='constancia_d'), path("verificacion-extemporanea/",views.verificacion_extemporanea,name="verificacion-extemporanea"), path('seleccion_cita/', views.seleccion_cita, name='seleccion_cita'), path("cancelar-cita/", views.cancelar, name="cancelar-cita")
]


