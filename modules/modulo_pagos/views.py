from django.shortcuts import render

# Create your views here.
def pagos(request):
    return render(request, './pagos.html')