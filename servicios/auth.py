from config import CONFIG
import requests
import json
from utils.storage import Storage


class Auth:
    def __init__(self):
        self.base_url = CONFIG.BASE_URL_PLANILLA
        self.storage = Storage()

    def sign_in(self, username, password):
        response = requests.post(f"{self.base_url}/login", json={'username': username, 'password': password})
        if response.status_code == 200:
            data = response.json()
            self.storage.save('access_token', data['token'])
            self.storage.save('user', data['user'])
            return True
        else:
            return False

    def sign_out(self):
        self.storage.delete('access_token')
        self.storage.delete('user')

    def get_access_token(self):
        return self.storage.load('access_token')

    def get_user(self):
        return self.storage.load('user')

    def check(self):
        return self.get_access_token() is not None
