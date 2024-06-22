from config import CONFIG
import requests
import json
from servicios.empresa_service import EmpresaService

class Auth:
    def __init__(self):
        self.base_url = CONFIG.BASE_URL_PLANILLA

        self.token = None
        self.user = None

    def sign_in(self, username, password):
        response = requests.post(f"{self.base_url}/login", json={'username': username, 'password': password})
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']
            self.user = data['user']
            return True
        else:
            return False

    def sign_out(self):
        self.token = None
        self.user = None

    def check(self):
        return self.token is not None
