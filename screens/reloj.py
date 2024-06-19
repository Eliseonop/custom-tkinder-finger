import customtkinter as ctk
from PIL import Image, ImageOps
from datetime import datetime
from controladores.device import Device
from base64 import b64decode
from io import BytesIO
import threading
import time
import locale
from screens.configuracion import Configuracion
from time import sleep
import asyncio

# Establecer la configuración regional en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


class Reloj(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.device = Device()
        self.huellas_capturadas = False
        self.procesar_huella = True
        self.initialize_ui_elements()
        self.start_threads()

    def initialize_ui_elements(self):
        subframe = ctk.CTkFrame(self)
        subframe.configure(height=50)
        subframe.pack(fill="x", side="top")

        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(50, 50))
        self.logo_label = ctk.CTkLabel(subframe, image=self.logo_image, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"), compound="left")
        self.logo_label.pack(side="left", padx=20, pady=(20, 10))

        self.label_title = ctk.CTkLabel(subframe, text="Tcontur Asistencia", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(side="left", padx=20, pady=(20, 10))

        self.label_dia = ctk.CTkLabel(subframe, text="", font=("Helvetica", 16), anchor='e')
        self.label_dia.pack(side="right", padx=20, pady=(20, 10))

        self.label_hora = ctk.CTkLabel(self, text="", font=("Helvetica", 100), anchor='center')
        self.label_hora.pack(padx=20, pady=20, fill="both", expand=True)

        boton_configuracion = ctk.CTkButton(self, text="Configuración", command=self.ir_a_configuracion)
        boton_configuracion.pack(padx=20, pady=20, side="bottom", anchor="e")
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="bottom", fill="x")
        self.image_label = None
        self.label_instruction = None
        self.label_result = None

    def ir_a_configuracion(self):
        self.master.on_page(Configuracion)

    def start_threads(self):
        threading.Thread(target=self.actualizar_reloj, daemon=True).start()
        threading.Thread(target=self.update_day, daemon=True).start()
        threading.Thread(target=self.load_huellas, daemon=True).start()

    def actualizar_reloj(self):
        while True:
            ahora = datetime.now()
            hora_formateada = ahora.strftime('%H:%M:%S')
            self.label_hora.configure(text=hora_formateada)
            time.sleep(1)

    def update_day(self):
        while True:
            ahora = datetime.now()
            dia_formateado = ahora.strftime('%A, %d de %B de %Y').capitalize()
            self.label_dia.configure(text=dia_formateado)
            time.sleep(1)

    def load_huellas(self):
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        carga = self.device.cargar_huellas()
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        if carga:

            threading.Thread(target=self.auth, daemon=True).start()
        else:
            self.label_result = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
            self.label_result.pack(padx=20, pady=20)

    def auth(self):
        while True:
            print("Esperando huella...")
            self.reset_ui()
            self.show_instruction("Ponga su dedo en el lector", "Esperando huella...")

            while True:
                try:
                    capture = self.device.zkfp2.AcquireFingerprint()
                    if capture:
                        print("Huella capturada")
                        self.process_fingerprint(capture)
                        # self.schedule_next_capture()
                        time.sleep(4)
                        break
                    # break
                except Exception as e:
                    print(f"Error al autenticar: {e}")

    def reset_ui(self):
        if self.image_label:
            self.image_label.pack_forget()
        if self.label_instruction:
            self.label_instruction.pack_forget()
        if self.label_result:
            self.label_result.pack_forget()

    def show_instruction(self, instruction_text, result_text):
        self.label_instruction = ctk.CTkLabel(self, text=instruction_text)
        self.label_instruction.pack(padx=10, pady=10)
        self.label_result = ctk.CTkLabel(self, text=result_text)
        self.label_result.pack(padx=10, pady=10)

    def process_fingerprint(self, capture):
        self.huellas_capturadas = True
        self.label_instruction.pack_forget()

        tmp, img = capture
        my_img = self.device.zkfp2.Blob2Base64String(img)
        decoded_temps = [b64decode(entry["template"]) for entry in self.device.listemp]
        datos_de_imagen = b64decode(my_img)
        imagen_bytes = BytesIO(datos_de_imagen)
        self.open_imagen = Image.open(imagen_bytes)

        for temp, entry in zip(decoded_temps, self.device.listemp):
            # self.progress_bar.step(20)
            match = self.device.zkfp2.DBMatch(tmp, temp)
            if match > 80:

                hora = datetime.now().strftime('%H:%M:%S')
                self.update_result("green",
                                   f"Usuario identificado: Score = {match} y empleado   {entry['empleado_name']} con ID = {entry['empleado']} - Hora: {hora}")
                break
            else:
                self.update_result("red", f"Usuario no identificado: Score = {match}")

        self.progress_bar.pack_forget()
        imagen_ctk = ctk.CTkImage(dark_image=self.filter_image, size=(200, 250))
        self.image_label = ctk.CTkLabel(self, image=imagen_ctk, text="", width=200, height=200)
        self.image_label.pack(padx=10, pady=10)

    def update_result(self, color, text):
        if color == "green":
            self.filter_image = ImageOps.colorize(self.open_imagen, "black", "#a7f3d0")
        else:
            self.filter_image = ImageOps.colorize(self.open_imagen, "black", "#fecaca")

        self.label_result.configure(text=text)

    # def schedule_next_capture(self):
    #     if self.huellas_capturadas:
    #         self.huellas_capturadas = False
    #         self.after(3000, self.auth)
