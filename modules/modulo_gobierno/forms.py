from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .models import Usuario
import re

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario de registro de usuario basado en UserCreationForm de Django.
    Permite registrar nuevos usuarios con datos adicionales como RFC y CURP.
    """

    acepto_terminos = forms.BooleanField(required=True, label="Acepto los términos y condiciones")
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'fecha_nacimiento', 'rfc', 'curp', 'password1', 'password2',
            'acepto_terminos'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'username': 'Nombre de usuario',
        }

    def clean_rfc(self):
        """
        Valida el formato del RFC ingresado.
        El RFC debe cumplir con la estructura oficial de México.
        """
        rfc = self.cleaned_data.get('rfc').upper()
        if not re.match('^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$', rfc):
            raise ValidationError('Formato de RFC con homoclave inválido')
        return rfc

    def clean_curp(self):
        """
        Valida el formato del CURP ingresado.
        El CURP debe cumplir con la estructura oficial de México.
        """
        curp = self.cleaned_data.get('curp').upper()
        if not re.match('^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$', curp):
            raise ValidationError('Formato de CURP inválido')
        return curp

    def clean(self):
        """
        Permite realizar validaciones adicionales antes de guardar el formulario.
        """
        cleaned_data = super().clean()
        return cleaned_data
