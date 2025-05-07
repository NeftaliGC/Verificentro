from django.shortcuts import render, redirect
from .models import Vehiculo, Cita
from .factories import VehiculoFactory

def verificacion(request):
    return render(request, "verificacion-vehicular.html")

def cancelar(request):
    return render(request, "cancelar-cita.html")

def holograma_exento(request):
    if request.method == 'POST':
        data = request.POST
        placa = data.get('placa', '').strip()
        serie = data.get('serie', '').strip()
        marca = data.get('marca', '').strip()
        submarca = data.get('submarca', '').strip()
        modelo = data.get('modelo', '').strip()
        nombre_solicitante = data.get('nombre_solicitante', '').strip()
        correo = data.get('correo', '').strip()

        # DEBUG: Imprimir los valores recibidos
        print(f"Placa: {placa}, Serie: {serie}, Marca: {marca}")

        if not placa:
            return render(request, 'verificacion-vehicular.html', {
                "error": "La placa es obligatoria."
            })

        vehiculo = VehiculoFactory.obtener_vehiculo(data)
        if vehiculo is None:
            return render(request, 'verificacion-vehicular.html', {
                "error": "Vehículo no encontrado. Verifica que los datos ingresados sean correctos."
            })

        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')
    
    return render(request, 'holograma-exento.html')

def constancia_d(request):
    if request.method == 'POST':
        data = request.POST
        placa = data.get('placa', '').strip()
        serie = data.get('serie', '').strip()
        marca = data.get('marca', '').strip()
        submarca = data.get('submarca', '').strip()
        modelo = data.get('modelo', '').strip()
        nombre_solicitante = data.get('nombre_solicitante', '').strip()
        correo = data.get('correo', '').strip()

        # DEBUG: Imprimir los valores recibidos
        print(f"Placa: {placa}, Serie: {serie}, Marca: {marca}")

        if not placa:
            return render(request, 'verificacion-vehicular.html', {
                "error": "La placa es obligatoria."
            })

        vehiculo = VehiculoFactory.obtener_vehiculo(data)
        if vehiculo is None:
            return render(request, 'verificacion-vehicular.html', {
                "error": "Vehículo no encontrado. Verifica que los datos ingresados sean correctos."
            })

        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')
    
    return render(request, "constancia-d.html")

def verificacion_extemporanea(request):
    if request.method == 'POST':
        data = request.POST
        placa = data.get('placa', '').strip()
        serie = data.get('serie', '').strip()
        marca = data.get('marca', '').strip()
        submarca = data.get('submarca', '').strip()
        modelo = data.get('modelo', '').strip()
        nombre_solicitante = data.get('nombre_solicitante', '').strip()
        correo = data.get('correo', '').strip()

        # DEBUG: Imprimir los valores recibidos
        print(f"Placa: {placa}, Serie: {serie}, Marca: {marca}")

        if not placa:
            return render(request, 'verificacion-vehicular.html', {
                "error": "La placa es obligatoria."
            })

        vehiculo = VehiculoFactory.obtener_vehiculo(data)
        if vehiculo is None:
            return render(request, 'verificacion-vehicular.html', {
                "error": "Vehículo no encontrado. Verifica que los datos ingresados sean correctos."
            })

        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')
    
    return render(request, "verificacion-extemporanea.html")

def index(request):
    return render(request, 'principal.html')

def citas(request):
    if request.method == 'POST':
        data = request.POST
        placa = data.get('placa', '').strip()
        serie = data.get('serie', '').strip()
        marca = data.get('marca', '').strip()
        submarca = data.get('submarca', '').strip()
        modelo = data.get('modelo', '').strip()
        nombre_solicitante = data.get('nombre_solicitante', '').strip()
        correo = data.get('correo', '').strip()

        try:
            vehiculo = Vehiculo.objects.get(
                placa=placa,
                serie=serie,
                marca=marca,
                submarca=submarca,
                modelo=modelo,
                dueño=nombre_solicitante,
                correo=correo
            )
        except Vehiculo.DoesNotExist:
            return render(request, 'verificacion-vehicular.html', {
                "error": "Vehículo no encontrado. Verifica que los datos ingresados sean correctos."
            })

        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')

    return render(request, 'verificacion-vehicular.html')

def seleccion_cita(request):
    if request.method == 'POST':
        # Recuperar el ID del vehículo desde la sesión
        vehiculo_id = request.session.get('vehiculo_id')
        if not vehiculo_id:
            return redirect('verificacion')

        municipio = request.POST.get('municipio')
        verificentro = request.POST.get('verificentro')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)

        # Crear la cita con el vehículo relacionado
        Cita.objects.create(
            vehiculo=vehiculo,
            municipio=municipio,
            verificentro=verificentro,
            fecha=fecha,
            hora=hora
        )

        # Eliminar la sesión después de agendar la cita
        del request.session['vehiculo_id']

        return redirect('index')

    else:
        vehiculo_id = request.session.get('vehiculo_id')
        if vehiculo_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            return render(request, 'citas.html', {'datos_cita': vehiculo})
        else:
            return redirect('verificacion')
