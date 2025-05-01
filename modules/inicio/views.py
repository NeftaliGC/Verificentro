from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages


# vistas principales
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')

# login usuario
def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido_paterno = request.POST['apellido_paterno']
        apellido_materno = request.POST['apellido_materno']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        contraseña = request.POST['contraseña']

        # Validación mínima
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('registro')

        usuario = Usuario(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            fecha_nacimiento=fecha_nacimiento,
            correo=correo,
            telefono=telefono,
            contraseña=contraseña  # Idealmente hasheada
        )
        usuario.save()
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('login')  # Cambia a donde rediriges después del registro

    return render(request, 'registro.html')
