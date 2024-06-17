# vistas/vista2.py

import customtkinter as ctk
from controladores.device import Device
from PIL import Image, ImageTk
from io import BytesIO
from base64 import b64encode, b64decode
import threading


class Marcar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(self, width=600, height=5)
        self.progress_bar.pack(side="top", )
        self.boton = ctk.CTkButton(self, text="Vista 2", command=self.destroy)
        self.boton.pack(padx=20, pady=20)

        self.device = Device()


        # self.progress_bar.set(0)

        self.load_huellas()

    def load_huellas(self):
        def load():
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            # aqui se hace la peticon de las uellas
            carga = self.device.cargar_huellas()
            # self.progress_bar.configure(mode="")
            self.progress_bar.pack_forget()  # Ocultar la barra de progreso

            if carga:
                self.boton_marcar = ctk.CTkButton(self, text="Probar Huellero", command=self.on_auth_huellas)
                self.boton_marcar.pack(padx=20, pady=20)
            else:
                print('No se han podido cargar las huellas')
                self.label = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
                self.label.pack(padx=20, pady=20)

        threading.Thread(target=load).start()

    def on_auth_huellas(self):
        def auth():
            while True:
                capture = self.device.zkfp2.AcquireFingerprint()
                if capture:
                    print('Huella dactilar capturada')
                    tmp, img = capture
                    my_img = self.device.zkfp2.Blob2Base64String(img)

                    datos_de_imagen = b64decode(my_img)
                    imagen_bytes = BytesIO(datos_de_imagen)
                    imagen = Image.open(imagen_bytes)

                    imagen = ctk.CTkImage(dark_image=imagen, size=(230, 230))
                    image_label = ctk.CTkLabel(self, image=imagen, text="", width=200, height=200)
                    image_label.pack(padx=10, pady=10)
                    break

        threading.Thread(target=auth).start()
