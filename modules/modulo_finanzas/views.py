from django.shortcuts import render
from django.views import View

class IngresoPlacaView(View):
    def get(self, request):
        return render(request, 'modulo_finanzas/ingreso_placa.html')

    def post(self, request):
        placa = request.POST.get('placa', '')
        
        return render(request, 'modulo_finanzas/resultado.html', {'placa': placa})