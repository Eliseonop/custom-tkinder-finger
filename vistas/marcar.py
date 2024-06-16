# vistas/vista2.py

import customtkinter as ctk
from controladores.device import Device
from PIL import Image, ImageTk
from io import BytesIO
from base64 import b64encode, b64decode


class Marcar(ctk.CTkFrame):
    def __init__(self, master, ):
        super().__init__(master, fg_color="transparent")
        self.boton = ctk.CTkButton(self, text="Vista 2", command=self.destroy)
        self.boton.pack(padx=20, pady=20)
        # if controlador is not None:
        self.device = Device()

        # self.controlador.probar_dispositivo()
        # self.controlador.cargar_huellas()
        self.auth_buttons()
        self.device.cargar_huellas()

    def auth_buttons(self):
        self.boton = ctk.CTkButton(self, text="Probar Huellero",
                                   command=self.auth_huellas)
        self.boton.pack(padx=20, pady=20)
        # if controlador is not None:

        # self.controlador.probar_dispositivo()

    def auth_huellas(self):

        while True:
            capture = self.device.zkfp2.AcquireFingerprint()
            if capture:
                print('Huella dactilar capturada')
                tmp, img = capture
                my_img = self.device.zkfp2.Blob2Base64String(img)

                datos_de_imagen = b64decode(my_img)

                # Crear un objeto de bytes
                imagen_bytes = BytesIO(datos_de_imagen)

                # Cargar la imagen desde los bytes usando Pillow
                imagen = Image.open(imagen_bytes)

                # imagen_tk = ImageTk.PhotoImage(imagen)

                # img2 = ImageTk.PhotoImage(img)
                # Crea un widget de etiqueta (label) y coloca la imagen en él
                imagen = ctk.CTkImage(dark_image=imagen, size=(230, 230))
                # label_imagen.pack(padx=20, pady=20)
                image_label = ctk.CTkLabel(self, image=imagen, text="", width=200, height=200)
                image_label.pack(padx=10, pady=10)
                break

