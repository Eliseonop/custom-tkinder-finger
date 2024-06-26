from config import CONFIG
import requests
from servicios.auth import Auth
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
import json
import os


class PlanillaService:
    def __init__(self, auth: Auth):
        self.base_url = CONFIG.BASE_URL_PLANILLA
        self.auth = auth
        self.empleados = []
        self.huellas = []
        self.marcaciones_offline = []

        self.load_marcaciones_offline()

        print("PlanillaService")
        print(self.auth.token)

    def post_marcacion(self, empleado, hora, save_offline=True):
        url = f"{self.base_url}/api/marcaciones"
        token = self.auth.obtener_token()
        headers = {
            'Authorization': f'Token {token}'
        }
        data = {
            'empleado': empleado['id'],
            'hora': hora
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(data)
            return True
        except requests.ConnectionError as e:
            print(f"Error de conexion: {e}")
            if save_offline:
                data_offline = {
                    'empleado': empleado['id'],
                    'nombre': empleado['nombre'],
                    'hora': hora
                }

                self.add_to_marcaciones_offline(data_offline)

            return False
        except requests.exceptions.RequestException as e:
            print(f"Error al guardar la marcación: {e}")
            return False

    def post_rectificar(self, empleado_id, hora):
        url = f"{self.base_url}/api/marcaciones/rectificar"
        token = self.auth.token
        headers = {
            'Authorization': f'Token {token}'
        }
        data = {
            'empleado': empleado_id,
            'hora': hora
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(response.json())
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error al guardar la marcación: {e}")
            return False

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

    def obtener_huellas(self):
        url = f"{self.base_url}/api/empleados/ver_huellas"
        token = self.auth.obtener_token()
        headers = {
            'Authorization': f'Token {token}'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.huellas = response.json()
            print(self.huellas)
            return True
        except requests.ConnectionError as e:
            self.huellas = self.storage.load('huellas', [])
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener las huellas: {e}")
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
            response = requests.put(url, headers=headers, json=data)
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

    def add_to_marcaciones_offline(self, data):
        self.marcaciones_offline.append(data)
        self.save_marcaciones_offline()

    def save_marcaciones_offline(self):
        with open('marcaciones_offline.json', 'w') as file:
            json.dump(self.marcaciones_offline, file, indent=4)

    def load_marcaciones_offline(self):
        if os.path.exists('marcaciones_offline.json'):
            with open('marcaciones_offline.json', 'r') as file:
                self.marcaciones_offline = json.load(file)
            return True
        else:
            return False
    def delete_marcacion_offline(self, empleado_id, hora):
        self.marcaciones_offline = [m for m in self.marcaciones_offline if not (m['empleado'] == empleado_id and m['hora'] == hora)]
        self.save_marcaciones_offline()