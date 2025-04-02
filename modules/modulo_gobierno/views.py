from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario, SolicitudValidacion
from .forms import RegistroUsuarioForm
from .services import validar_con_gobierno
import json

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Guardar usuario sin activar todavía
            usuario = form.save(commit=False)
            usuario.is_active = False  # No activo hasta validación
            usuario.save()
            
            # Crear solicitud de validación
            solicitud = SolicitudValidacion.objects.create(usuario=usuario)
            
            # Validar con módulo de gobierno (servicio externo)
            datos_validacion = {
                'nombre': f"{usuario.first_name} {usuario.last_name}",
                'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%Y-%m-%d'),
                'rfc': usuario.rfc,
                'curp': usuario.curp
            }
            
            resultado = validar_con_gobierno(datos_validacion)
            
            if resultado.get('valido'):
                solicitud.aprobar(resultado)
                usuario.is_active = True
                usuario.verificado_gobierno = True
                usuario.save()
                enviar_notificacion(usuario, aprobado=True)
                messages.success(request, '¡Registro exitoso! Su cuenta ha sido validada.')
                login(request, usuario)
                return redirect('inicio')
            else:
                solicitud.rechazar(resultado, resultado.get('motivo'))
                enviar_notificacion(usuario, aprobado=False, motivo=resultado.get('motivo'))
                messages.error(request, f"Registro rechazado: {resultado.get('motivo')}")
                return redirect('registro')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registro/registro.html', {'form': form})

def enviar_notificacion(usuario, aprobado, motivo=None):
    asunto = "Resultado de validación de registro"
    
    if aprobado:
        mensaje = f"""
        Estimado {usuario.first_name}:
        
        Su registro ha sido aprobado satisfactoriamente.
        Ahora puede acceder a todos los servicios del sistema.
        
        Datos de su cuenta:
        Usuario: {usuario.username}
        Nombre: {usuario.get_full_name()}
        
        Saludos,
        Equipo de Gobierno
        """
    else:
        mensaje = f"""
        Estimado {usuario.first_name}:
        
        Lamentamos informarle que su registro no pudo ser aprobado.
        Motivo: {motivo}
        
        Por favor verifique sus datos e intente nuevamente.
        
        Saludos,
        Equipo de Gobierno
        """
    
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        fail_silently=False,
    )