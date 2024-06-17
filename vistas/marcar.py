# vistas/vista2.py

import customtkinter as ctk
from controladores.device import Device
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
from base64 import b64decode
import threading


class Marcar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="top")

        self.boton = ctk.CTkButton(self, text="Vista 2", command=self.destroy)
        self.boton.pack(padx=20, pady=20)

        self.device = Device()
        self.image_label = None
        self.label_instruction = None
        self.label_result = None

        self.load_huellas()

    def load_huellas(self):
        def load():
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            carga = self.device.cargar_huellas()
            self.progress_bar.pack_forget()

            if carga:
                self.boton_marcar = ctk.CTkButton(self, text="Marcar Asistencia", command=self.on_auth_huellas)
                self.boton_marcar.pack(padx=20, pady=20)
            else:
                self.label = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
                self.label.pack(padx=20, pady=20)

        threading.Thread(target=load).start()

    def on_auth_huellas(self):
        def auth():
            # Clear previous labels
            if self.image_label:
                self.image_label.pack_forget()
            if self.label_instruction:
                self.label_instruction.pack_forget()
            if self.label_result:
                self.label_result.pack_forget()

            self.label_instruction = ctk.CTkLabel(self, text="Ponga su dedo en el lector")
            self.label_instruction.pack(padx=10, pady=10)
            self.label_result = ctk.CTkLabel(self, text="Esperando huella...")
            self.label_result.pack(padx=10, pady=10)

            while True:
                capture = self.device.zkfp2.AcquireFingerprint()
                if capture:
                    self.label_instruction.pack_forget()
                    tmp, img = capture
                    my_img = self.device.zkfp2.Blob2Base64String(img)

                    # Decoding templates
                    decoded_temps = [b64decode(entry["template"]) for entry in self.device.listemp]

                    # Process the captured image
                    datos_de_imagen = b64decode(my_img)
                    imagen_bytes = BytesIO(datos_de_imagen)
                    open_imagen = Image.open(imagen_bytes)

                    for temp, entry in zip(decoded_temps, self.device.listemp):
                        match = self.device.zkfp2.DBMatch(tmp, temp)

                        if match > 80:
                            self.filter_image = ImageOps.colorize(open_imagen, "black", (50, 205, 50))  # Green color
                            self.label_result.configure(
                                text=f"Usuario identificado: Score = {match} y empleado {entry['empleado_name']} con ID = {entry['empleado']}"
                            )
                            break
                        else:
                            self.filter_image = ImageOps.colorize(open_imagen, "black", "red")
                            self.label_result.configure(text=f"Usuario no identificado: Score = {match}")

                    imagen_ctk = ctk.CTkImage(dark_image=self.filter_image, size=(200, 250))
                    self.image_label = ctk.CTkLabel(self, image=imagen_ctk, text="", width=200, height=200)
                    self.image_label.pack(padx=10, pady=10)
                    break

        threading.Thread(target=auth).start()
