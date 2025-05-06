from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario
from django.contrib import messages


# vistas principales
def home(request):
    return render(request, 'home.html')

def registro(request):
    return render(request, 'registro.html')

# registro usuario
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

#login usuario
def login_usuario(request):  # <-- nuevo nombre
    if request.method == 'POST':
        correo = request.POST.get('username')
        contrasena = request.POST.get('password')

        user = authenticate(request, email=correo, password=contrasena)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas.'})

    return render(request, 'login.html')


# panel de usuario
def panel_usuario(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redirige si no hay sesión

    return render(request, 'panel_usuario.html')

# cerrar sesion
def logout(request):
    request.session.flush()
    return redirect('login')
