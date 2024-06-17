import customtkinter as ctk
from tkinter import StringVar
from servicios.empleados_service import EmpleadosService
from servicios.auth import Auth
import threading
from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image
from pyzkfp import ZKFP2
from servicios.finger_service import FingerService


class SubirTemplate(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.initialize_ui_elements()
        self.initialize_fingerprint_device()
        self.initialize_services()

        self.lista_empleados = []
        self.nombres_empleados = []
        self.selected_template = None
        self.selected_empleado = None

        self.load_empleados()

    def initialize_ui_elements(self):
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="top", pady=2)
        self.image_label = None
        self.fingerprint_message_label = None

    def initialize_fingerprint_device(self):
        self.zkfp2 = ZKFP2()
        self.zkfp2.Init()
        device_count = self.zkfp2.GetDeviceCount()
        if device_count > 0:
            print(f"{device_count} dispositivos encontrados")
            self.device = self.zkfp2.OpenDevice(0)
        else:
            self.device = None
            print("No se encontraron dispositivos")

    def initialize_services(self):
        auth = Auth()
        self.empleados_service = EmpleadosService(auth)
        self.finger_service = FingerService(auth)

    def load_empleados(self):
        threading.Thread(target=self.load_empleados_thread).start()

    def load_empleados_thread(self):
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        if self.empleados_service.obtener_empleados():
            self.lista_empleados = self.empleados_service.empleados
            self.nombres_empleados = ["Ninguno"] + [empleado['nombre'] for empleado in self.lista_empleados]
            self.initialize_main_template()
            self.initialize_finger_template()
        else:
            print('No se han podido cargar las huellas')
            self.display_message("No se han podido cargar las huellas")

        self.progress_bar.pack_forget()

    def initialize_main_template(self):
        self.display_message("Subir Huella Digital")
        self.display_message("Buscar Empleado", pady=2)

        self.var = StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.var)
        self.entry.pack(padx=20, pady=2)
        self.entry.bind('<KeyRelease>', self.check_autocomplete)

        self.optionmenu_var = StringVar(value="Ninguno")
        self.optionmenu = ctk.CTkOptionMenu(self, variable=self.optionmenu_var, values=self.nombres_empleados,
                                            command=self.optionmenu_callback)
        self.optionmenu.pack(padx=20, pady=20)
        self.update_optionmenu(self.nombres_empleados)

        self.submit_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.submit_button_frame.pack(side="bottom", pady=20)

        self.submit_button = ctk.CTkButton(self.submit_button_frame, text="Registrar", command=self.submit_form,
                                           state="disabled", fg_color="#4338ca")
        self.submit_button.pack(padx=20, pady=20)

    def initialize_finger_template(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(padx=20, pady=20)
        self.boton_capture = ctk.CTkButton(button_frame, text="Capturar Huella", command=self.capture_fingerprint)
        self.boton_capture.pack(side="left", padx=10)

    def capture_fingerprint(self):
        self.show_fingerprint_message("Poner Dedo en Huellero")

        templates, imgs = self.acquire_fingerprint_data()
        if templates and imgs:
            self.selected_template = b64encode(bytes(templates[0])).decode()
            self.write_img(imgs[0])
            self.update_submit_button_state()

        self.hide_fingerprint_message()

    def acquire_fingerprint_data(self):
        templates, imgs = [], []
        while True:
            capture = self.zkfp2.AcquireFingerprint()
            if capture:
                print('Huella dactilar capturada')
                templates.append(capture[0])
                imgs.append(capture[1])
                break
        return templates, imgs

    def show_fingerprint_message(self, message):
        if self.image_label:
            self.image_label.pack_forget()
        if not self.fingerprint_message_label:
            self.fingerprint_message_label = ctk.CTkLabel(self, text=message)
        else:
            self.fingerprint_message_label.configure(text=message)
        self.fingerprint_message_label.pack(pady=10)
        self.update()

    def hide_fingerprint_message(self):
        if self.fingerprint_message_label:
            self.fingerprint_message_label.pack_forget()

    def write_img(self, img):
        my_img = self.zkfp2.Blob2Base64String(img)
        datos_de_imagen = b64decode(my_img)
        imagen_bytes = BytesIO(datos_de_imagen)
        imagen = Image.open(imagen_bytes)
        ctk_image = ctk.CTkImage(dark_image=imagen, size=(200, 250))

        if self.image_label:
            self.image_label.configure(image=ctk_image)
        else:
            self.image_label = ctk.CTkLabel(self, image=ctk_image, text="", width=200, height=200)
        self.image_label.pack(padx=10, pady=10)

    def display_message(self, message, pady=20):
        label = ctk.CTkLabel(self, text=message)
        label.pack(padx=20, pady=pady)

    def check_autocomplete(self, event):
        typed = self.var.get().lower()
        data = ["Ninguno"] + [item for item in self.nombres_empleados if
                              typed in item.lower()] if typed else self.nombres_empleados
        self.update_optionmenu(data)

    def update_optionmenu(self, data):
        self.optionmenu.configure(values=data)
        self.optionmenu_var.set(data[0] if data else '')

    def optionmenu_callback(self, choice):
        self.selected_empleado = next((empleado for empleado in self.lista_empleados if empleado['nombre'] == choice),
                                      None) if choice != "Ninguno" else None
        self.update_submit_button_state()

    def update_submit_button_state(self):
        self.submit_button.configure(
            state="normal" if self.selected_empleado and self.selected_template else "disabled")

    def submit_form(self):
        if not self.selected_empleado:
            print("No se ha seleccionado ningún empleado")
            return

        datos = {
            "empleado": self.selected_empleado['id'],
            "empleado_name": self.selected_empleado['nombre'],
            "template": self.selected_template
        }

        print("Enviando datos:", datos)
        self.finger_service.push_finger(datos)
