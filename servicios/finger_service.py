from config import CONFIG
import requests
from servicios.auth import Auth


class FingerService:
    def __init__(self, auth: Auth):
        self.base_url = CONFIG.BASE_URL_HUELLAS
        self.auth = auth
        self.empleados = []

    def push_finger(self, data: {
        "empleado": int,
        "empleado_name": str,
        "template": str
    }):
        url = f"{self.base_url}"
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print(response.json())
                print(f"Huella dactilar registrada y enviada al servidor con ID = {data['empleado']}")
                return True
            else:
                print(f"Error al enviar la huella dactilar al servidor: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los empleados: {e}")
            return False

#     empleados = Empleados(auth)
#     lista_empleados = empleados.obtener_empleados()
#     print(lista_empleados)
