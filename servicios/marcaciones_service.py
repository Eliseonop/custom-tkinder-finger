# from servicios.auth import Auth
# from config import CONFIG
# import requests
# import json
# import os
#
#
# class MarcacionesService:
#     def __init__(self, auth: Auth):
#         self.base_url = CONFIG.BASE_URL_PLANILLA
#         self.auth = auth
#         self.marcaciones_offline = []
#
#     def create_marcacion(self, data: {
#         "empleado": int,
#         "hora": str,
#     }):
#         url = f"{self.base_url}/api/marcaciones"
#         token = self.auth.get_access_token()
#         headers = {
#             'Authorization': f'Token {token}'
#         }
#
#         try:
#             response = requests.post(url, json=data, headers=headers)
#             print('que paso')
#             print(response.json())
#             if response.status_code == 201:
#                 print(response.json())
#                 print(f"Marcación registrada y enviada al servidor con ID = {data['empleado']}")
#                 return True
#             else:
#                 print(f"Error al enviar la marcación al servidor: {response.status_code}")
#                 return False
#
#         except requests.ConnectionError as e:
#
#             print(f"Error de conexión al enviar la marcación al servidor: {e}")
#             self.add_to_marcaciones_offline(data)
#             return False
#
#
#         except requests.exceptions.RequestException as e:
#             print(f"Error al enviar la marcación al servidor: {e}")
#             return False
#
#     def add_to_marcaciones_offline(self, data):
#         self.marcaciones_offline.append(data)
#         self.save_marcaciones_offline()
#
#     def save_marcaciones_offline(self):
#         with open('marcaciones_offline.json', 'w') as file:
#             json.dump(self.marcaciones_offline, file, indent=4)
#
#     def load_marcaciones_offline(self):
#         if os.path.exists('marcaciones_offline.json'):
#             with open('marcaciones_offline.json', 'r') as file:
#                 self.marcaciones_offline = json.load(file)
#             return True
#         else:
#             return False
