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
from screens.auth_window import AuthWindow
from servicios.marcaciones_service import MarcacionesService
from servicios.auth import Auth
from datetime import datetime

# Establecer la configuración regional en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from servicios.planilla_service import PlanillaService


class Reloj(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.auth = Auth()
        self.device = Device()
        self.planilla_service = PlanillaService(self.auth)
        # self.marcaciones_service = MarcacionesService()
        self.huellas_capturadas = False
        self.procesar_huella = True
        self.initialize_ui_elements()

        self.is_active = True
        # if threading.enumerate() == 1:
        #

        print(threading.active_count())
        # for thread in threading.enumerate():
        #     if thread is not threading.current_thread():
        #         # thread.join()
        #         print(f"Deteniendo hilo {thread.is_alive()} {thread}")
        self.print_active_threads_and_check_duplicates()
        # if threading.active_count() > 1:
        self.start_threads()

    def print_active_threads_and_check_duplicates(self):
        active_threads = threading.enumerate()
        thread_names = set()
        duplicates = []

        print("Hilos activos:")
        for thread in active_threads:
            print(f"Nombre: {thread.name}, Identificador: {thread.ident}")
            if thread.name in thread_names:
                duplicates.append(thread.name)
            else:
                thread_names.add(thread.name)

        if duplicates:
            print("\nHilos duplicados encontrados:")
            for name in duplicates:
                print(name)
        else:
            print("\nNo se encontraron hilos duplicados.")

    def destroy(self):
        self.is_active = False

        super().destroy()

    def destroy_threads(self):
        print("Destruyendo Reloj")
        self.is_active = False
        for thread in threading.enumerate():
            if thread is not threading.current_thread():
                # thread.join()
                print(f"Deteniendo hilo {thread.is_alive()} {thread}")
        # super().destroy()
        #
        # for thread in threading.enumerate():
        #     if thread is not threading.current_thread():
        #         # thread.
        #         print(f"Deteniendo hilo {thread}")

    def initialize_ui_elements(self):
        subframe = ctk.CTkFrame(self)
        subframe.configure(height=50)

        subframe.pack(fill="x", side="top")

        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(50, 50))
        self.logo_label = ctk.CTkLabel(subframe, image=self.logo_image, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"), compound="left")
        self.logo_label.pack(side="left", padx=20, pady=(20, 10))

        self.label_title = ctk.CTkLabel(subframe, text="Tcontur Asistencia", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_title.pack(side="left", padx=20, pady=(20, 10))

        self.label_dia = ctk.CTkLabel(subframe, text="", font=("Helvetica", 18), anchor='e')
        self.label_dia.pack(side="right", padx=20, pady=(20, 10))

        self.label_hora = ctk.CTkLabel(self, text="", font=("Helvetica", 120), anchor='center')
        self.label_hora.pack(padx=20, pady=20, fill="both", expand=True)

        new_image = ctk.CTkImage(Image.open("fabricacion.png"), size=(30, 30),
                                 )

        boton_configuracion = ctk.CTkButton(self, text="", command=self.ir_a_configuracion,
                                            width=10, height=30,
                                            corner_radius=90,
                                            fg_color="transparent", bg_color="transparent",
                                            border_spacing=10,
                                            image=new_image)
        boton_configuracion.bind("<Enter>", lambda e: print("Mouse sobre el botón"))
        boton_configuracion.pack(padx=20, pady=20, side="bottom", anchor="e")
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=5)
        self.progress_bar.pack(side="bottom", pady=60)
        self.image_label = None
        self.label_instruction = None
        self.label_result = None

    def ir_a_configuracion(self):
        self.is_active = False
        self.destroy()
        self.master.on_page(Configuracion)
        # self.destroy()

    def start_threads(self):

        # if threading.active_count() == 1:

        threading.Thread(target=self.actualizar_reloj, daemon=True).start()
        threading.Thread(target=self.update_day, daemon=True).start()
        threading.Thread(target=self.load_huellas, daemon=True).start()

    def actualizar_reloj(self):
        while self.is_active:
            ahora = datetime.now()
            hora_formateada = ahora.strftime('%H:%M:%S')
            self.label_hora.configure(text=hora_formateada)

            time.sleep(1)

    def update_day(self):
        while self.is_active:
            ahora = datetime.now()
            dia_formateado = ahora.strftime('%A, %d de %B de %Y').capitalize()
            self.label_dia.configure(text=dia_formateado)
            time.sleep(1)

    def load_huellas(self):

        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        try:
            print("Cargando huellas")
            carga = self.planilla_service.obtener_huellas()
            print("Huellas cargadas")
            self.progress_bar.stop()
            print("Deteniendo progress bar")
            self.progress_bar.pack_forget()

            if carga:
                print("Huellas cargadas --- inciando auth")
                threading.Thread(target=self.hacer_marcacion()).start()
            else:
                self.label_result = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
                self.label_result.pack(padx=20, pady=20)
                self.boton_autenticar = ctk.CTkButton(self, text="Autenticar", command=self.go_to_autenticar)
                self.boton_autenticar.pack(padx=20, pady=20)

        except Exception as e:
            print(f"Error al cargar huellas: {e}")

    def go_to_autenticar(self):
        self.master.on_page(AuthWindow)

    def hacer_marcacion(self):
        while self.is_active:
            print("Esperando huella...")
            self.reset_ui()
            self.show_instruction("Ponga su dedo en el lector", "Esperando huella...")

            while self.is_active:
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
        decoded_temps = [b64decode(entry["huella"]) for entry in self.planilla_service.huellas]
        datos_de_imagen = b64decode(my_img)
        imagen_bytes = BytesIO(datos_de_imagen)
        self.open_imagen = Image.open(imagen_bytes)

        for temp, entry in zip(decoded_temps, self.planilla_service.huellas):
            # self.progress_bar.step(20)
            match = self.device.zkfp2.DBMatch(tmp, temp)
            if match > 70:
                # threading.Thread(target=self.planilla_service.post_marcacion, args=(entry["id"], datetime.now().astimezone().isoformat())).start()

                result = self.planilla_service.post_marcacion(entry["id"], datetime.now().astimezone().isoformat())
                hora = datetime.now().strftime('%H:%M:%S')
                if result:
                    self.update_result("green",
                                       f"Usuario identificado: {entry['nombre']} - {hora}")
                else:
                    self.update_result("red", f"Usuario no identificado: Score = {match}")
                # self.update_result("green",
                #                    f"Usuario identificado: {entry['nombre']} ")
                break
            else:
                self.update_result("red", f"Usuario no identificado: Score = {match}")

        self.progress_bar.pack_forget()
        imagen_ctk = ctk.CTkImage(light_image=self.filter_image, dark_image=self.filter_image, size=(200, 250))
        self.image_label = ctk.CTkLabel(self, image=imagen_ctk, text="", width=200, height=200)
        self.image_label.pack(padx=10, pady=10)

    def make_marcaje(self):
        try:
            self.planilla_service.marcar_asistencia()
        except Exception as e:
            print(f"Error al marcar asistencia: {e}")

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
