from django.shortcuts import render, redirect
from .models import Empleado
from django.contrib import messages

# Vista de inicio de sesión del empleado
def login_empleado(request):
    if request.method == 'POST':
        numero_cuenta = request.POST.get('numero_cuenta')
        contrasena = request.POST.get('password')

        try:
            empleado = Empleado.objects.get(numero_cuenta=numero_cuenta)
            if empleado.contrasena == contrasena:
                request.session['empleado_id'] = empleado.id
                request.session['empleado_nombre'] = empleado.nombre
                messages.success(request, f'¡Bienvenido, {empleado.nombre}!')
                return redirect('panel_empleado')  # Asegúrate de tener esta URL configurada
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Empleado.DoesNotExist:
            messages.error(request, 'Número de cuenta no registrado.')

    return render(request, 'login_empleado.html')


# Panel del empleado
def panel_empleado(request):
    if 'empleado_id' not in request.session:
        return redirect('login_empleado')  # Redirige si no ha iniciado sesión

    return render(request, 'panel_empleado.html')


# Cerrar sesión (se recomienda cambiar nombre para no solaparlo con logout del usuario)
def logout_empleado(request):
    request.session.flush()
    return redirect('login_empleado')
