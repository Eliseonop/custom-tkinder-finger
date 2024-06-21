from config import CONFIG
import requests
from servicios.auth import Auth


class PlanillaService:
    def __init__(self, auth: Auth):
        self.base_url = CONFIG.BASE_URL_PLANILLA
        self.auth = auth
        self.empleados = []

    def obtener_empleados(self):
        url = f"{self.base_url}/api/empleados"
        token = self.auth.get_access_token()
        headers = {
            'Authorization': f'Token {token}'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 200 OK
            self.empleados = response.json()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los empleados: {e}")
            return False
