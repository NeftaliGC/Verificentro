# Librerías estándar
from datetime import date, datetime
from decimal import Decimal

# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.contrib.staticfiles import finders

# Terceros
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm

# Locales
from modules.inicio.models import Normativa, Vehiculo, Verificacion

# ======================= VISTAS PRINCIPALES =======================

def panel_regulaciones(request):
    return render(request, 'principalRegulaciones.html')

# ======================= CRUD Normativas =======================

def listar_normativas(request):
    normativas = Normativa.objects.all().order_by('-vigente_desde')
    return render(request, 'listar_normativas.html', {'normativas': normativas})

def nueva_normativa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        tipo_combustible = request.POST.get('tipo_combustible')
        limite_co = request.POST.get('limite_co')
        limite_nox = request.POST.get('limite_nox')
        usa_obd = request.POST.get('usa_obd') == '1'
        frecuencia_meses = request.POST.get('frecuencia_meses')
        vigente_desde = request.POST.get('vigente_desde')
        vigente_hasta = request.POST.get('vigente_hasta') or None

        Normativa.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            tipo_combustible=tipo_combustible,
            limite_co=limite_co,
            limite_nox=limite_nox,
            usa_obd=usa_obd,
            frecuencia_meses=frecuencia_meses,
            vigente_desde=parse_date(vigente_desde),
            vigente_hasta=parse_date(vigente_hasta) if vigente_hasta else None,
        )
        return redirect('listar_normativas')

    return render(request, 'nueva-normativa.html')

def editar_normativa(request, pk):
    normativa = get_object_or_404(Normativa, pk=pk)

    if request.method == 'POST':
        normativa.nombre = request.POST.get('nombre')
        normativa.descripcion = request.POST.get('descripcion')
        normativa.tipo_combustible = request.POST.get('tipo_combustible')
        normativa.limite_co = request.POST.get('limite_co')
        normativa.limite_nox = request.POST.get('limite_nox')
        normativa.usa_obd = bool(int(request.POST.get('usa_obd')))
        normativa.frecuencia_meses = request.POST.get('frecuencia_meses')
        normativa.vigente_desde = request.POST.get('vigente_desde')
        normativa.vigente_hasta = request.POST.get('vigente_hasta') or None
        normativa.save()
        return redirect('listar_normativas')

    return render(request, 'editar_normativa.html', {'normativa': normativa})

def eliminar_normativa(request, pk):
    normativa = get_object_or_404(Normativa, pk=pk)

    if request.method == 'POST':
        normativa.delete()
        return redirect('listar_normativas')

    return render(request, 'eliminar_normativa.html', {'normativa': normativa})

# ======================= Verificación Vehicular =======================
def verificacion_vehicular(request):
    resultado = None
    datos_verificacion = None

    if 'placa' in request.GET:
        placa = request.GET['placa'].upper().strip()
        try:
            vehiculo = Vehiculo.objects.get(placa=placa)
            normativa = Normativa.objects.filter(
                tipo_combustible=vehiculo.tipo_combustible,
                vigente_desde__lte=date.today()
            ).filter(
                Q(vigente_hasta__gte=date.today()) | Q(vigente_hasta__isnull=True)
            ).first()

            if normativa:
                try:
                    co_medido = Decimal(request.GET.get('co_medido', 0))
                    nox_medido = Decimal(request.GET.get('nox_medido', 0))
                    obd_funciona = request.GET.get('obd_funciona', 'false') == 'true'
                except (ValueError, TypeError) as e:
                    resultado = f"⚠️ Error al procesar los valores de las emisiones: {str(e)}"
                    return render(request, 'verificacion_vehicular.html', {
                        'resultado': resultado,
                        'vehiculo': vehiculo
                    })

                # Actualizar valores medidos en el vehículo
                vehiculo.co_medido = co_medido
                vehiculo.nox_medido = nox_medido
                vehiculo.save()


                # Crear registro de verificación
                verificacion = Verificacion.objects.create(
                    placa=vehiculo,
                    fecha=date.today(),
                    co_emitido=co_medido,
                    nox_emitido=nox_medido,
                    obd_funciona=obd_funciona,
                    normativa_aplicada=normativa,
                    aprobada=False
                )

                # Evaluar si cumple con la normativa
                cumple_co = co_medido <= normativa.limite_co
                cumple_nox = nox_medido <= normativa.limite_nox
                cumple_obd = obd_funciona == normativa.usa_obd
                cumple = cumple_co and cumple_nox and cumple_obd

                verificacion.aprobada = cumple
                verificacion.save()

                # Preparar datos para mostrar
                datos_verificacion = {
                    'vehiculo': vehiculo,
                    'normativa': normativa,
                    'co_medido': co_medido,
                    'nox_medido': nox_medido,
                    'obd_funciona': obd_funciona,
                    'cumple_co': cumple_co,
                    'cumple_nox': cumple_nox,
                    'cumple_obd': cumple_obd,
                    'aprobado': cumple,
                    'fecha': date.today().strftime('%d/%m/%Y')
                }

                resultado = '✅ Aprobado' if cumple else '❌ Rechazado'
            else:
                resultado = '⚠️ No hay normativa aplicable al vehículo.'
        except Vehiculo.DoesNotExist:
            resultado = '🚫 Vehículo no encontrado.'

    return render(request, 'verificacion_vehicular.html', {
        'resultado': resultado,
        'datos': datos_verificacion
    })

# ======================= Reportes =======================

def reportes(request):
    return render(request, 'reportes.html')

# === Reporte: Vehículos Aprobados ===

def reporte_vehiculos_aprobados(request):
    return generar_reporte_verificaciones(request, True, 'vehiculos_aprobados.pdf', "Reporte de Vehículos Aprobados")

# === Reporte: Vehículos Rechazados ===

def reporte_vehiculos_rechazados(request):
    return generar_reporte_verificaciones(request, False, 'vehiculos_rechazados.pdf', "Reporte de Vehículos Rechazados")

# ======================= Funciones auxiliares para reportes =======================

def generar_reporte_verificaciones(request, aprobadas, filename, titulo):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    agregar_encabezado_reporte(elements, titulo)

    verificaciones = Verificacion.objects.filter(aprobada=aprobadas).select_related('placa')

    if not verificaciones.exists():
        elements.append(Paragraph("No hay vehículos registrados.", styles['Normal']))
    else:
        data = [['Placa', 'Marca', 'Modelo', 'Año', 'CO', 'NOx', 'Fecha']]
        for verificacion in verificaciones:
            data.append([
                verificacion.placa.placa,
                verificacion.placa.marca,
                verificacion.placa.modelo,
                str(verificacion.placa.anio),
                f"{verificacion.co_emitido} ppm",
                f"{verificacion.nox_emitido} ppm",
                verificacion.fecha.strftime('%d/%m/%Y')
            ])

        tabla_reporte(elements, data)

    doc.build(elements, onFirstPage=agregar_numero_pagina, onLaterPages=agregar_numero_pagina)
    return response

def agregar_encabezado_reporte(elements, titulo):
    styles = getSampleStyleSheet()
    logo_path = finders.find('imagenes/logo-reporte.png')
    if logo_path:
        logo = Image(logo_path)
        logo.drawHeight = (logo.imageHeight / logo.imageWidth) * (2 * inch)
        logo.drawWidth = 2 * inch
        logo.hAlign = 'LEFT'
        elements.append(logo)

    elements.append(Paragraph(titulo, styles['Title']))
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Paragraph(f"Fecha de generación: {fecha}", styles['Normal']))
    elements.append(Spacer(1, 20))

def tabla_reporte(elements, data, encabezado_color='#004aad'):
    table = Table(data, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(encabezado_color)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.whitesmoke]),
    ]))
    elements.append(table)

def agregar_numero_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_number_text = f"Página {doc.page}"
    canvas.drawRightString(200 * mm, 15 * mm, page_number_text)
    canvas.restoreState()