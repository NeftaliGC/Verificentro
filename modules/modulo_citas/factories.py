from .models import Vehiculo

class VehiculoFactory:
    @staticmethod
    def crear_desde_post(data):
        return Vehiculo(
            placa=data.get('placa', '').strip(),
            serie=data.get('serie', '').strip(),
            marca=data.get('marca', '').strip(),
            submarca=data.get('submarca', '').strip(),
            modelo=data.get('modelo', '').strip(),
            dueño=data.get('nombre_solicitante', '').strip(),
            correo=data.get('correo', '').strip()
        )
