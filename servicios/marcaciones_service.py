from servicios.auth import Auth
from config import CONFIG
import requests


class MarcacionesService:
    def __init__(self, auth: Auth):
        self.base_url = CONFIG.BASE_URL_PLANILLA
        self.auth = auth

    def create_marcacion(self, data: {
        "empleado": int,
        "hora": str,
    }):
        url = f"{self.base_url}/api/marcaciones"
        token = self.auth.get_access_token()
        headers = {
            'Authorization': f'Token {token}'
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            print(response.json())
            if response.status_code == 201:
                print(response.json())
                print(f"Marcación registrada y enviada al servidor con ID = {data['empleado']}")
                return True
            else:
                print(f"Error al enviar la marcación al servidor: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error al enviar la marcación al servidor: {e}")
            return False
