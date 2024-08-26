from typing import Any

import requests
from requests import ConnectionError, RequestException

from servicios.auth import Auth
from CTkMessagebox import CTkMessagebox
from servicios.empresa_service import EmpresaService
from modelos.error_code import CodeResponse
from utils.storage import Storage
from utils.config import CONFIG
from utils.logger import Logger


class PlanillaService:
    def __init__(self, auth: Auth):
        self.base_url = CONFIG.API_URL_GENERAL
        self.empresa_service = EmpresaService()
        self.new_url = None
        self.auth = auth
        self.empleados = []
        self.huellas = []
        self.marcaciones_offline = []
        self.storage = Storage()
        self.logger = Logger()

        self.create_new_url()
        self.load_marcaciones_offline()

    def create_new_url(self):
        empresa = self.empresa_service.get_empresa_storage()

        if empresa is None:
            self.new_url = ""
        else:
            self.new_url = f"https://{empresa['codigo'] + self.base_url}"

    def post_marcacion(self, empleado, hora, save_offline=True) -> tuple[CodeResponse, Any] | tuple[
        CodeResponse, ConnectionError] | tuple[CodeResponse, RequestException]:
        url = f"{self.new_url}/api/marcaciones"
        token = self.auth.obtener_token()
        print(token)
        headers = {
            'Authorization': f'Token {token}'
        }
        data = {
            'empleado': empleado['id'],
            'hora': hora
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            print(response.request.headers)
            # print(response.status_code)

            if response.status_code == 201:
                # self.delete_marcacion_offline(empleado['id'], hora)
                return CodeResponse.SUCCESS, response.json()
            if response.status_code == 400:
                # print('error 400')
                self.logger.save_log_error(response.json())

                if response.json()['error_class'] == 'ValidationError':
                    # CTkMessagebox(title="Error", message=f"{response.json()}",
                    #               icon="warning")
                    return CodeResponse.VALIDATION_ERROR, response.json()

                return CodeResponse.ERROR, response.json()

            if response.status_code == 401:
                if save_offline:
                    data_offline = {
                        'empleado': empleado['id'],
                        'nombre': empleado['nombre'],
                        'hora': hora
                    }

                    self.add_to_marcaciones_offline(data_offline)

                # CTkMessagebox(title="Error de autenticación", message="No tiene permisos para marcar.",
                #               icon="warning")

                return CodeResponse.UNAUTHORIZED, response.json()
            return CodeResponse.ERROR, response.json()

        except requests.ConnectionError as e:
            print(f"Error de conexion: {e}")
            if save_offline:
                data_offline = {
                    'empleado': empleado['id'],
                    'nombre': empleado['nombre'],
                    'hora': hora
                }

                self.add_to_marcaciones_offline(data_offline)

            return CodeResponse.OFFLINE, e
        except requests.exceptions.RequestException as e:
            print(requests.get(url).json())
            print(f"Error al guardar la marcación: {e}")
            return CodeResponse.ERROR, e

    def post_rectificar(self, empleado_id, hora) -> CodeResponse:
        url = f"{self.new_url}/api/marcaciones/rectificar"
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
            return CodeResponse.SUCCESS

        except requests.exceptions.RequestException as e:
            print(f"Error al guardar la marcación: {e}")
            return CodeResponse.ERROR

    def obtener_empleados(self):
        url = f"{self.new_url}/api/empleados"
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

    def obtener_huellas(self) -> CodeResponse:
        self.empresa_service.view_message_if_not_empresa()

        url = f"{self.new_url}/api/empleados/ver_huellas"
        token = self.auth.obtener_token()
        headers = {
            'Authorization': f'Token {token}'
        }
        try:
            response = requests.get(url, headers=headers)
            # response.raise_for_status()
            if response.status_code == 200:
                self.huellas = response.json()
                self.storage.save('huellas', self.huellas)
                return CodeResponse.SUCCESS
            if response.status_code == 401:
                self.huellas = self.storage.load('huellas', [])

                # CTkMessagebox(title="Error de autenticación", message="No tiene permisos para ver las huellas.",
                #               icon="warning")

                return CodeResponse.UNAUTHORIZED

            CTkMessagebox(title="Error", message="Error de Servidor.",
                          icon="warning")
            self.huellas = self.storage.load('huellas', [])

            return CodeResponse.ERROR

        except requests.ConnectionError as e:
            self.huellas = self.storage.load('huellas', [])
            print(self.huellas)
            return CodeResponse.OFFLINE
        # except requests.exceptions.RequestException as e:
        #     print(f"Error al obtener las huellas: {e}")
        #     self.huellas = self.storage.load('huellas', [])
        #     return ErrorCode.ERROR

    def upload_huella(self, empleado_id, huella):
        url = f"{self.new_url}/api/empleados/{empleado_id}/guardar_huella"
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
            CTkMessagebox(title="Error al subir la huella!", message=details['detail']['message'],
                          icon="warning", option_1="Cancelar")
            print(f"Error al subir la huella: {e}")
            return False

    def add_to_marcaciones_offline(self, data):
        self.marcaciones_offline.append(data)
        self.save_marcaciones_offline()

    def save_marcaciones_offline(self):
        self.storage.save('marcaciones_offline', self.marcaciones_offline)

    def load_marcaciones_offline(self):
        self.marcaciones_offline = self.storage.load('marcaciones_offline', [])

    def delete_marcacion_offline(self, empleado_id, hora):
        self.marcaciones_offline = [m for m in self.marcaciones_offline if
                                    not (m['empleado'] == empleado_id and m['hora'] == hora)]
        self.save_marcaciones_offline()
