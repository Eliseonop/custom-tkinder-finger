import customtkinter as ctk
from tkinter import StringVar
from servicios.empleadosservice import EmpleadosService
from servicios.auth import Auth
import threading
from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image
from pyzkfp import ZKFP2


class SubirTemplate(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.progress_bar = ctk.CTkProgressBar(self, width=600, height=5)
        self.progress_bar.pack(side="top", pady=2)
        self.zkfp2 = ZKFP2()
        self.zkfp2.Init()
        device_count = self.zkfp2.GetDeviceCount()

        if device_count > 0:
            print(f"{device_count} dispositivos encontrados")
            self.device = self.zkfp2.OpenDevice(0)
        else:
            self.device = None
            print("No se encontraron dispositivos")

        auth = Auth()
        self.empleados_service = EmpleadosService(auth)
        self.lista_empleados = []
        self.nombres_empleados = []
        self.selected_template = None
        self.selected_empleado = None
        self.image_label = None
        self.fingerprint_message_label = None  # Referencia al label del mensaje
        self.load_empleados()

    def finger_template(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(padx=20, pady=20)

        self.boton_capture = ctk.CTkButton(button_frame, text="Capturar Huella", command=self.capture_fingerprint)
        self.boton_capture.pack(side="left", padx=10)

    def capture_fingerprint(self):
        # Mostrar el mensaje de "Poner Dedo en Huellero"
        if self.image_label is not None:
            self.image_label.pack_forget()


        if self.fingerprint_message_label is None:
            self.fingerprint_message_label = ctk.CTkLabel(self, text="Poner Dedo en Huellero")
            self.fingerprint_message_label.pack(pady=10)
        else:
            self.fingerprint_message_label.configure(text="Poner Dedo en Huellero")
            self.fingerprint_message_label.pack(pady=10)

        self.update()

        templates = []
        imgs = []
        while True:
            capture = self.zkfp2.AcquireFingerprint()
            if capture:
                print('Huella dactilar capturada')
                tmp, img = capture
                templates.append(tmp)
                imgs.append(img)
                break

        # Ocultar el mensaje de "Poner Dedo en Huellero"
        self.fingerprint_message_label.pack_forget()

        base64_templates = b64encode(bytes(templates[0])).decode()
        self.selected_template = base64_templates

        self.write_img(imgs[0])
        self.update_submit_button_state()

    def write_img(self, img):
        my_img = self.zkfp2.Blob2Base64String(img)
        datos_de_imagen = b64decode(my_img)
        imagen_bytes = BytesIO(datos_de_imagen)
        imagen = Image.open(imagen_bytes)

        imagen = ctk.CTkImage(dark_image=imagen, size=(200, 250))

        if self.image_label is not None:
            self.image_label.configure(image=imagen)
            self.image_label.pack(padx=10, pady=10)
        else:
            self.image_label = ctk.CTkLabel(self, image=imagen, text="", width=200, height=200)
            self.image_label.pack(padx=10, pady=10)

    def load_empleados(self):
        def load():
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()

            carga = self.empleados_service.obtener_empleados()

            self.progress_bar.pack_forget()

            if carga:
                self.lista_empleados = self.empleados_service.empleados
                self.nombres_empleados = ["Ninguno"] + [empleado['nombre'] for empleado in self.lista_empleados]
                self.template_principal()
                self.finger_template()
            else:
                print('No se han podido cargar las huellas')
                self.label = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
                self.label.pack(padx=20, pady=20)

        threading.Thread(target=load).start()

    def template_principal(self):
        self.label = ctk.CTkLabel(self, text="Subir Huella Digital")
        self.label.pack(padx=20, pady=20)

        self.search_label = ctk.CTkLabel(self, text="Buscar Empleado")
        self.search_label.pack(padx=20, pady=2)

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

    def check_autocomplete(self, event):
        typed = self.var.get()
        if (typed == ''):
            data = self.nombres_empleados
        else:
            data = ["Ninguno"] + [item for item in self.nombres_empleados if typed.lower() in item.lower()]
        self.update_optionmenu(data)

    def update_optionmenu(self, data):
        self.optionmenu.configure(values=data)
        if data:
            self.optionmenu_var.set(data[0])
        else:
            self.optionmenu_var.set('')

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        if choice == "Ninguno":
            self.selected_empleado = None
        else:
            self.selected_empleado = next(
                (empleado for empleado in self.lista_empleados if empleado['nombre'] == choice), None)
        self.update_submit_button_state()

    def update_submit_button_state(self):
        if self.selected_empleado and self.selected_template:
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    def submit_form(self):
        if not self.selected_empleado:
            print("No se ha seleccionado ningún empleado")
            return

        empleado_id = self.selected_empleado['id']
        empleado_nombre = self.selected_empleado['nombre']
        template = self.selected_template

        datos = {
            "id": empleado_id,
            "empleado": empleado_nombre,
            "template": template
        }

        print("Enviando datos:", datos)
        # Aquí se realizaría el POST con la biblioteca adecuada, por ejemplo requests
        # response = requests.post(url, json=datos)
        # print("Response:", response.json())
