from django.core.management.base import BaseCommand
# Asegúrate de usar la ruta COMPLETA:
from modules.modulo_finanzas.gui.interfaz import InterfazFinanzas

class Command(BaseCommand):
    help = "Lanza la interfaz gráfica de finanzas"

    def handle(self, *args, **options):
        try:
            app = InterfazFinanzas()
            app.ejecutar()
        except Exception as e:
            self.stderr.write(f"Error: {str(e)}")  # Para ver errores detallados