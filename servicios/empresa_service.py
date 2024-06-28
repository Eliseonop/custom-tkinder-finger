import requests
from utils.storage import Storage
from CTkMessagebox import CTkMessagebox
import os
from utils.config import CONFIG


class EmpresaService:
    def __init__(self):
        self.base_url = CONFIG.API_URL_URBANITO
        self.storage = Storage()
        self.empresas = []

    def get_empresas(self) -> bool:
        url = f"{self.base_url}/tracker/empresas"

        try:
            response = requests.get(url)
            response.raise_for_status()
            self.empresas = response.json()
            print(self.empresas)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener las empresas: {e}")
            return False

    def save_empresa_storage(self, empresa):
        self.storage.save('empresa', empresa)

    def get_empresa_storage(self):
        return self.storage.load('empresa')

    def view_message_if_not_empresa(self):
        if not self.get_empresa_storage():
            CTkMessagebox(title="Empresa no seleccionada",
                          message="Por favor, vaya a configuración y seleccione una empresa.",
                          icon="warning")
