import django
import os

# Configura Django para usar el ORM desde la GUI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

# Exporta la clase principal para facilitar imports
from .interfaz import InterfazFinanzas