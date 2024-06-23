from config import CONFIG
import requests
import json
from servicios.empresa_service import EmpresaService
from utils.storage import Storage


class Auth:
    def __init__(self):
        self.base_url = CONFIG.API_URL_GENERAL
        self.empresa_service = EmpresaService()
        self.token = None
        self.user = None
        self.storage = Storage()

    def sign_in(self, username, password):
        if not self.empresa_service.get_empresa_storage():
            return
        empresa = self.empresa_service.get_empresa_storage()
        url = f"https://{empresa['codigo'] + self.base_url}"
        response = requests.post(f"{url}/login",
                                 json={'username': username, 'password': password})
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']
            self.user = data['user']

            self.storage.save('token', self.token)
            return True
        else:
            return False

    def obtener_token(self):
        return self.storage.load('token')

    def sign_out(self):
        self.token = None
        self.user = None

    def check(self):
        return self.token is not None
