from django.shortcuts import render

# Create your views here.
def pagos(request):
    return render(request, './pagos.html')

def pagar(request, tipo_pago):
    if tipo_pago == 'multa':
        return render(request, './pagar_multa.html')
    elif tipo_pago == 'verificacion':
        return render(request, './pagar_verificacion.html')
    else:
        return render(request, './404_pago.html')