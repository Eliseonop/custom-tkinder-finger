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
from time import sleep


class SubirTemplate(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.initialize_ui_elements()
        self.initialize_fingerprint_device()
        self.initialize_services()

        self.lista_empleados = []
        self.filtered_empleados = []
        self.selected_template = None
        self.selected_empleado = None

        self.frame_action = None
        self.scroll_height = 250
        self.load_empleados()

    def initialize_ui_elements(self):
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="top", pady=2, fill="x")

        self.label_buscar = ctk.CTkLabel(self, text="Buscar Empleado")
        self.label_buscar.pack(padx=20, pady=2)

        self.var = StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.var)
        self.entry.pack(padx=20, pady=2)
        self.entry.bind('<KeyRelease>', self.check_autocomplete)

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
        threading.Thread(target=self.load_empleados_thread, daemon=True).start()

    def load_empleados_thread(self):
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        if self.empleados_service.obtener_empleados():
            sleep(1)
            self.lista_empleados = self.empleados_service.empleados
            self.filtered_empleados = self.lista_empleados
            self.initialize_main_template()
            # self.initialize_finger_template()
        else:
            print('No se han podido cargar las huellas')
            self.display_message("No se han podido cargar las huellas")

        self.progress_bar.pack_forget()

    def initialize_main_template(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=self.scroll_height)
        self.scrollable_frame.pack(padx=20, pady=10)

        self.create_employee_table()

    def create_employee_table(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Nombre", "Acciones"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        for i, empleado in enumerate(self.filtered_empleados, start=1):
            label = ctk.CTkLabel(self.scrollable_frame, text=empleado['nombre'], width=300)
            label.grid(row=i, column=0, padx=5, pady=5)

            register_button = ctk.CTkButton(self.scrollable_frame, text="Registrar Huella",
                                            command=lambda e=empleado: threading.Thread(target=self.capture_fingerprint,
                                                                                        args=(e,)).start())
            register_button.grid(row=i, column=1, padx=5, pady=5)

    def initialize_finger_template(self):
        self.frame_action = ctk.CTkFrame(self)
        self.frame_action.pack(pady=20)

        self.capture_button = ctk.CTkButton(self.frame_action, text="Reintentar", command=self.capture_fingerprint)
        self.capture_button.pack(padx=20, pady=20, side="left")

        self.cancel_button = ctk.CTkButton(self.frame_action, text="Cancelar", command=self.cancelar)
        self.cancel_button.pack(padx=20, pady=20, side="left")

        self.submit_button = ctk.CTkButton(self.frame_action, text="Registrar", command=self.submit_form,
                                           fg_color="indigo")
        self.submit_button.pack(padx=20, pady=20, side="left")

    def capture_fingerprint(self, empleado=None):
        print("Capturando huella")
        print(self.selected_empleado)

        if self.frame_action is not None:
            self.frame_action.pack_forget()

        if empleado:
            self.selected_empleado = empleado

        self.show_fingerprint_message(
            f"Por favor, coloque su dedo en el lector de huellas, {self.selected_empleado['nombre']}.")

        templates, imgs = self.acquire_fingerprint_data()
        if templates and imgs:
            self.selected_template = b64encode(bytes(templates[0])).decode()
            self.write_img(imgs[0])
            self.initialize_finger_template()

        self.hide_fingerprint_message()

    def cancelar(self):
        self.selected_empleado = None
        self.selected_template = None
        if self.image_label:
            self.image_label.pack_forget()
            self.image_label = None
        if self.frame_action:
            self.frame_action.pack_forget()
            self.frame_action = None
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
            self.fingerprint_message_label = ctk.CTkLabel(self, text=message, font=("Arial", 12, "bold"))
        else:
            self.fingerprint_message_label.configure(text=message)
        self.fingerprint_message_label.pack(pady=10, padx=10 * 2)
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

    def update_submit_button_state(self):
        if self.selected_empleado and self.selected_template:
            self.capture_button.configure(state="normal")
        else:
            self.capture_button.configure(state="disabled")

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
        threading.Thread(target=self.finger_service.push_finger, args=(datos,)).start()

    def eliminar_huella(self, empleado_id):
        print(f"Eliminando huella del empleado con ID: {empleado_id}")
        threading.Thread(target=self.finger_service.delete_finger, args=(empleado_id,)).start()

    def check_autocomplete(self, event):
        typed = self.var.get().lower()
        self.filtered_empleados = [empleado for empleado in self.lista_empleados if typed in empleado['nombre'].lower()]
        self.create_employee_table()
