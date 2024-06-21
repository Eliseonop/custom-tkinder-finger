from pyzkfp import ZKFP2
from base64 import b64encode, b64decode
import requests
import time
from modelos.huellas import Huellas
from config import CONFIG
from utils.storage import Storage


class Device:
    def __init__(self):
        # self.app = app
        self.zkfp2 = ZKFP2()
        self.zkfp2.Init()
        device_count = self.zkfp2.GetDeviceCount()
        self.storage = Storage()

        self.img = None
        self.device = None

        self.listemp = []
        self.url = CONFIG.BASE_URL_HUELLAS
        if device_count > 0:
            print(f"{device_count} dispositivos encontrados")
            self.device = self.zkfp2.OpenDevice(0)

        else:
            self.device = None
            print("No se encontraron dispositivos")
            # exit()

        self.listemp: list(Huellas) = []

    def set_token(self, token):
        self.storage.save('token_huella', token)

    def get_token(self):
        return self.storage.load('token_huella')

    def info_dispositivo(self):
        cantidad_dispositivos = self.zkfp2.GetDeviceCount()

        return cantidad_dispositivos

    def probar_dispositivo(self) -> str:
        self.zkfp2.Light('green')
        time.sleep(0.09)
        self.zkfp2.Light('red')
        time.sleep(0.09)
        self.zkfp2.Light('blue')
        time.sleep(0.09)

        my_img: str = ""

        while True:
            capture = self.zkfp2.AcquireFingerprint()
            if capture:
                print('Huella dactilar capturada')
                tmp, img = capture
                my_img = self.zkfp2.Blob2Base64String(img)

            break
        return my_img

    def registrar_huella(self):
        print("Coloca tu dedo en el escáner para registrar...")
        templates = []

        self.zkfp2.Light('green')
        time.sleep(0.09)
        for i in range(2):
            while True:
                capture = self.zkfp2.AcquireFingerprint()
                if capture:
                    print('Huella dactilar capturada')
                    tmp, img = capture
                    templates.append(tmp)
                    break

        base64_templates = b64encode(bytes(templates[0])).decode()

        finger_id = int(input("Ingrese el ID de usuario para registrar: "))

        try:
            data = {
                "empleado": finger_id,
                "template": base64_templates
            }
            response = requests.post(self.url, json=data)

            if response.status_code == 201:
                print(response.json())
                print(f"Huella dactilar registrada y enviada al servidor con ID = {finger_id}")
            else:
                print(f"Error al enviar la huella dactilar al servidor: {response.status_code}")

            print(f"Huella dactilar registrada con ID = {finger_id}")
        except Exception as e:
            print(f"Error al registrar la huella: {e}")

    def cargar_huellas(self):
        print(self.get_token() + "token")
        try:

            response = requests.get(self.url)

            if response.status_code == 200:
                newlist = response.json()
                for entry in newlist:
                    self.listemp.append(entry)
                    # self.listemp.append(Huellas(entry["id"], entry["empleado"], entry["template"]))
                print("Huellas dactilares cargadas correctamente")
                print(self.listemp)
                return True
            else:
                print(f"Error al cargar las huellas dactilares del servidor: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error al cargar las huellas dactilares: {e}")
            return False

    def autenticar_usuario(self) -> str:

        while True:
            capture = self.zkfp2.AcquireFingerprint()
            if capture:
                tmp, img = capture
                print("Huella dactilar capturada para autenticación")
                start_time = time.time()

                print("Coloca tu dedo en el escáner para autenticación...")
                print(self.listemp)

                decoded_temps = [b64decode(entry["template"]) for entry in self.listemp]

                for temp, entry in zip(decoded_temps, self.listemp):
                    match = self.zkfp2.DBMatch(tmp, temp)
                    if match > 80:
                        print(
                            f"Usuario identificado: ID = {entry["id"]} , Score = {match} y empleado {entry["empleado"]}")
                        # self.zkfp2.show_image(img)
                        self.img = img

                    else:
                        print(f"Usuario no identificado: Score = {match}")
                        # self.zkfp2.show_image(img)
                    break
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Tiempo transcurrido: {elapsed_time} segundos")
                break
            # self.img = img
            break

        return self.zkfp2.Blob2Base64String(self.img)
