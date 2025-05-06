from django.urls import path
from . import views

urlpatterns = [

    path('', views.pagos, name='pagos'),
    path('pagar/<str:tipo_pago>/', views.pagar, name='pagar'),

]