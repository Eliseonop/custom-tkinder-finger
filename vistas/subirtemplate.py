import customtkinter as ctk
from tkinter import StringVar
from controladores.device import Device
from servicios.empleadosservice import EmpleadosService
from servicios.auth import Auth
import threading
from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image


class SubirTemplate(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(self, width=600, height=5)
        self.progress_bar.pack(side="top", pady=2)

        auth = Auth()
        self.device = Device()
        self.empleados_service = EmpleadosService(auth)
        self.lista_empleados = []
        self.nombres_empleados = []
        self.load_empleados()

    def button_fingerprint(self):
        self.boton = ctk.CTkButton(self, text="Capturar Huella", command=self.capture_fingerprint, state="disabled")
        self.boton.pack(padx=20, pady=20)

    def capture_fingerprint(self):
        templates = []
        imgs = []
        for i in range(2):
            while True:
                capture = self.device.zkfp2.AcquireFingerprint()
                if capture:
                    print('Huella dactilar capturada')
                    tmp, img = capture
                    templates.append(tmp)
                    imgs.append(img)
                    break
        base64_templates = b64encode(bytes(templates[0])).decode()
        self.selected_template = base64_templates

        self.write_img(imgs[0])
        pass

    def write_img(self, img):
        my_img = self.device.zkfp2.Blob2Base64String(img)
        datos_de_imagen = b64decode(my_img)
        imagen_bytes = BytesIO(datos_de_imagen)
        imagen = Image.open(imagen_bytes)

        imagen = ctk.CTkImage(dark_image=imagen, size=(230, 230))
        image_label = ctk.CTkLabel(self, image=imagen, text="", width=200, height=200)
        image_label.pack(padx=10, pady=10)

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

            else:
                print('No se han podido cargar las huellas')
                self.label = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
                self.label.pack(padx=20, pady=20)

        threading.Thread(target=load).start()

    def template_principal(self):
        self.label = ctk.CTkLabel(self, text="Subir Huella Digital")
        self.label.pack(padx=20, pady=20)

        self.var = StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.var)
        self.entry.pack(padx=20, pady=2)
        self.entry.bind('<KeyRelease>', self.check_autocomplete)

        self.optionmenu_var = StringVar(value="Ninguno")
        self.optionmenu = ctk.CTkOptionMenu(self, variable=self.optionmenu_var, values=self.nombres_empleados,
                                            command=self.optionmenu_callback)
        self.optionmenu.pack(padx=20, pady=20)

        self.update_optionmenu(self.nombres_empleados)

        # Botón para realizar el POST, inicialmente deshabilitado
        self.submit_button = ctk.CTkButton(self, text="Enviar", command=self.submit_form, state="disabled")
        self.submit_button.pack(padx=20, pady=20)

    def check_autocomplete(self, event):
        typed = self.var.get()
        if typed == '':
            data = self.nombres_empleados
        else:
            data = ["Ninguno"] + [item for item in self.nombres_empleados if typed.lower() in item.lower()]
        self.update_optionmenu(data)

    def update_optionmenu(self, data):
        # Clear current options
        self.optionmenu.configure(values=data)
        if data:
            self.optionmenu_var.set(data[0])
        else:
            self.optionmenu_var.set('')

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        # Deshabilitar el botón "Enviar" si la opción seleccionada es "Ninguno"
        if choice == "Ninguno":
            self.submit_button.configure(state="disabled")
            self.selected_empleado = None
        else:
            self.submit_button.configure(state="normal")
            # Guardar el empleado seleccionado
            self.selected_empleado = next(
                (empleado for empleado in self.lista_empleados if empleado['nombre'] == choice), None)

    def submit_form(self):
        if not hasattr(self, 'selected_empleado') or self.selected_empleado is None:
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

        # Realizar el POST (Aquí deberías usar la librería adecuada para tu backend, por ejemplo requests)
        print("Enviando datos:", datos)
        # response = requests.post(url, json=datos)
        # print("Response:", response.json())
