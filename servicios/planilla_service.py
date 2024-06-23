from config import CONFIG
import requests
from servicios.auth import Auth
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox


class PlanillaService:
    def __init__(self, auth: Auth):
        self.base_url = CONFIG.BASE_URL_PLANILLA
        self.auth = auth
        self.empleados = []

    def obtener_empleados(self):
        url = f"{self.base_url}/api/empleados"
        token = self.auth.token
        print(token)
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

    def upload_huella(self, empleado_id, huella):
        url = f"{self.base_url}/api/empleados/{empleado_id}/guardar_huella"
        token = self.auth.token
        headers = {
            'Authorization': f'Token {token}'
        }
        data = {
            'huella': huella
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            details = e.response.json()
            # print('json')
            print(details)
            # messagebox.showerror("Error", )

            CTkMessagebox(title="Error al subir la huella!", message=details['detail']['message'],
                          icon="warning", option_1="Cancelar")
            # messagebox.showerror("Error", "Error al subir la huella")

            print(f"Error al subir la huella: {e}")
            return False
