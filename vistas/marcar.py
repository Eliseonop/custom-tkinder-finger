# vistas/vista2.py

import customtkinter as ctk
from controladores.device import Device
from PIL import Image, ImageTk
from io import BytesIO
import base64


class Marcar(ctk.CTkFrame):
    def __init__(self, master, ):
        super().__init__(master, fg_color="transparent")
        self.boton = ctk.CTkButton(self, text="Vista 2", command=self.destroy)
        self.boton.pack(padx=20, pady=20)
        # if controlador is not None:
        # self.controlador = controlador

        # self.controlador.probar_dispositivo()
        # self.controlador.cargar_huellas()
        self.auth_buttons()

    def auth_buttons(self):
        self.boton = ctk.CTkButton(self, text="Probar Huellero",
                                   command=self.auth_huellas)
        self.boton.pack(padx=20, pady=20)
        # if controlador is not None:

        # self.controlador.probar_dispositivo()

    def auth_huellas(self):
        pass
    #     img = self.controlador.autenticar_usuario()
    #     if img is not None:
    #         # Convierte la imagen en un objeto Image de Pillow
    #         datos_de_imagen = base64.b64decode(img)
    #
    #         # Crear un objeto de bytes
    #         imagen_bytes = BytesIO(datos_de_imagen)
    #
    #         # Cargar la imagen desde los bytes usando Pillow
    #         imagen = Image.open(imagen_bytes)
    #
    #         imagen_tk = ImageTk.PhotoImage(imagen)
    #
    #         # img2 = ImageTk.PhotoImage(img)
    #         # Crea un widget de etiqueta (label) y coloca la imagen en él
    #         imagen = ctk.CTkImage(dark_image=imagen, size=(230, 230))
    #         # label_imagen.pack(padx=20, pady=20)
    #         image_label = ctk.CTkLabel(self, image=imagen, text="", width=200, height=200)
    #         image_label.pack(padx=10, pady=10)
    #     else:
    #         print("No se pudo autenticar")
