import customtkinter as ctk
from PIL import Image, ImageOps
from controladores.device import Device
from base64 import b64decode
from io import BytesIO
import threading
import time
import locale
from screens.configuracion import Configuracion
from screens.auth_reloj import Auth_Reloj
from servicios.auth import Auth
from datetime import datetime
from servicios.planilla_service import PlanillaService
from utils.logger import Logger
from modelos.error_code import CodeResponse
from resource_path import RUTA_LOGO, RUTA_FABRICACION
from CTkMessagebox import CTkMessagebox
from modelos.marcacion import Marcacion

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


class Reloj(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.progress_bar = None
        self.label_mark = None
        self.label_auth = None
        self.pack(fill="both", expand=True)
        self.auth = Auth()
        self.device = Device()
        self.logger = Logger()

        self.planilla_service = PlanillaService(self.auth)
        # self.marcaciones_service = MarcacionesService()
        self.huellas_capturadas = False
        self.procesar_huella = True
        self.initialize_ui_elements()
        self.is_active_huella = True
        self.is_active_reloj = True
        print(threading.active_count())

        self.start_threads()
        self.toplevel_window = None

    def destroy(self):
        self.is_active_huella = False
        self.is_active_reloj = False
        super().destroy()

    def initialize_ui_elements(self):
        subframe = ctk.CTkFrame(self)
        subframe.configure(height=50)

        subframe.pack(fill="x", side="top")

        self.logo_image = ctk.CTkImage(Image.open(RUTA_LOGO), size=(50, 50))
        self.logo_label = ctk.CTkLabel(subframe, image=self.logo_image, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"), compound="left")
        self.logo_label.pack(side="left", padx=20, pady=(20, 10))

        self.label_title = ctk.CTkLabel(subframe, text="Tcontur Asistencia", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_title.pack(side="left", padx=20, pady=(20, 10))

        self.label_dia = ctk.CTkLabel(subframe, text="", font=("Helvetica", 18), anchor='e')
        self.label_dia.pack(side="right", padx=20, pady=(20, 10))

        self.label_hora = ctk.CTkLabel(self, text="", font=("Helvetica", 120), anchor='center')
        self.label_hora.pack(padx=20, pady=20, fill="both", expand=True)

        new_image = ctk.CTkImage(Image.open(RUTA_FABRICACION), size=(30, 30),

                                 )

        boton_configuracion = ctk.CTkButton(self, text="", command=self.ir_a_configuracion,
                                            width=10, height=10,
                                            corner_radius=75,
                                            fg_color="transparent", bg_color="transparent",
                                            border_spacing=0,

                                            # hover_color="#0ea5e9",
                                            text_color="white",
                                            # hover=False,
                                            border_color="black",
                                            image=new_image)
        # boton_configuracion.bind("<Enter>", lambda e: print("Mouse sobre el botón"))
        boton_configuracion.pack(padx=20, pady=20, side="bottom", anchor="e")

        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=5)
        self.progress_bar.pack(side="bottom", pady=60)
        self.image_label = None
        self.label_instruction = None
        self.label_result = None

    def ir_a_configuracion(self):
        # self.is_active_huella = False

        self.destroy()
        self.master.on_page(Configuracion)
        # self.destroy()

    def start_threads(self):

        threading.Thread(target=self.actualizar_reloj, daemon=True).start()
        threading.Thread(target=self.update_day, daemon=True).start()
        threading.Thread(target=self.load_huellas, daemon=True).start()

    def actualizar_reloj(self):
        while self.is_active_reloj:
            ahora = datetime.now()
            hora_formateada = ahora.strftime('%H:%M:%S')
            self.label_hora.configure(text=hora_formateada)

            time.sleep(1)

    def update_day(self):
        while self.is_active_reloj:
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
            print(self.planilla_service.huellas)
            print(carga)
            if self.planilla_service.huellas:
                if carga == CodeResponse.UNAUTHORIZED:
                    self.label_auth = ctk.CTkLabel(self, text="Autenticar",
                                                   font=ctk.CTkFont(size=12, weight="bold"),
                                                   fg_color="red")
                    self.label_auth.configure(corner_radius=10)
                    self.label_auth.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-60)
                # threading.Thread(target=self.esperar_huella()).start()

                if carga == CodeResponse.OFFLINE:
                    print("off line")
                    # self.label_result = ctk.CTkLabel(self, text="Modo offline activo")
                    # self.label_result.pack(padx=20, pady=20)
                    self.label_offline = ctk.CTkLabel(self, text="Offline", font=ctk.CTkFont(size=12, weight="bold"),
                                                      fg_color="red")
                    self.label_offline.configure(corner_radius=10)
                    self.label_offline.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)

                    # threading.Thread(target=self.esperar_huella()).start()

                threading.Thread(target=self.esperar_huella()).start()
            elif carga == CodeResponse.UNAUTHORIZED:
                self.label_result = ctk.CTkLabel(self, text="No hay huellas registradas",
                                                 text_color="blue",
                                                 font=ctk.CTkFont(size=16, weight="normal"))
                self.label_result.pack(padx=20, pady=20)


            elif carga == CodeResponse.ERROR:
                self.label_result = ctk.CTkLabel(self, text="No se han podido cargar las huellas")
                self.label_result.pack(padx=20, pady=20)
                # self.boton_autenticar = ctk.CTkButton(self, text="Autenticar", command=self.go_to_autenticar)
                # self.boton_autenticar.pack(padx=20, pady=20)
            # if carga == ErrorCode.SUCCESS:
            #     threading.Thread(target=self.esperar_huella()).start()



        except Exception as e:
            print(f"Error al cargar huellas: {e}")

    #

    def go_to_autenticar(self):
        self.master.on_page(Auth_Reloj)

    def esperar_huella(self):
        self.logger.save_log_info("-----------------------Esperando huella-----------------------")
        while self.is_active_huella:
            # print("Esperando huella...")
            self.reset_ui()
            self.show_instruction("Ponga su dedo en el lector", "Esperando huella...")

            while self.is_active_huella:
                try:
                    capture = self.device.zkfp2.AcquireFingerprint()
                    if capture:
                        print("Huella capturada")
                        self.process_fingerprint(capture)

                        time.sleep(4)
                        break
                    # break
                except Exception as e:
                    print(f"Error al autenticar: {e}")
                    self.is_active_huella = False
                    # Cerrar la aplicacion hubo un error con el dispositivo
                    self.reset_ui()
                    CTkMessagebox(title="Error Device",
                                  message="Por favor, verifique la conectividad del dispositivo o asegúrese de que no haya otras aplicaciones utilizando el mismo recurso.",
                                  icon="warning",
                                  sound=True
                                  )
                    # cerrar la aplicacion
                    # self.
                    # self.destroy()
                    self.label_result = ctk.CTkLabel(self, text="Hubo un error con el dispositivo", text_color="red",
                                                     font=ctk.CTkFont(size=16, weight="normal")
                                                     )
                    self.label_result.pack(padx=20, pady=20)

                    break

    def reset_ui(self):
        if self.image_label:
            self.image_label.pack_forget()
        if self.label_instruction:
            self.label_instruction.pack_forget()
        if self.label_result:
            self.label_result.pack_forget()
        if self.label_mark:
            self.label_mark.pack_forget()

    def show_instruction(self, instruction_text, result_text):
        self.label_instruction = ctk.CTkLabel(self, text=instruction_text)
        self.label_instruction.pack(padx=10, pady=10)
        self.label_result = ctk.CTkLabel(self, text=result_text)
        self.label_result.pack(padx=10, pady=10)
        self.label_mark = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=22, weight="bold"))

    def process_fingerprint(self, capture):
        self.huellas_capturadas = True
        self.label_instruction.pack_forget()
        self.label_result.pack_forget()
        self.label_mark.pack_forget()
        tmp, img = capture
        my_img = self.device.zkfp2.Blob2Base64String(img)
        decoded_temps = [b64decode(entry["huella"]) for entry in self.planilla_service.huellas]
        datos_de_imagen = b64decode(my_img)
        imagen_bytes = BytesIO(datos_de_imagen)
        self.open_imagen = Image.open(imagen_bytes)
        match_found = False
        # print("Huellas cargadas")
        # print(self.planilla_service.huellas)

        for temp, entry in zip(decoded_temps, self.planilla_service.huellas):
            # self.progress_bar.step(20)
            match = self.device.zkfp2.DBMatch(tmp, temp)
            print(f"Match: {match}")
            if match > 80:
                match_found = True
                self.view_progress()
                print(f"Empleado identificado: {entry}")
                result, data = self.planilla_service.post_marcacion(entry, datetime.now().astimezone().isoformat())
                self.stop_progress()
                print(f"Resultado: {result}")
                if result == CodeResponse.SUCCESS or result == CodeResponse.OFFLINE:
                    newMarcacion = Marcacion(data)
                    text_marca = "Entrada" if newMarcacion.entrada else "Salida"
                    color_marca = "#6ee7b7" if data["entrada"] else "#7dd3fc"
                    self.update_result(
                        label1=f"Marcando... ",
                        c_label1='#334155',
                        c_huella=color_marca,
                        c_mark=color_marca,
                        t_mark=text_marca,
                    )

                    # self.update_result(result, f"Marcando... ", newMarcacion.entrada)
                if result == CodeResponse.VALIDATION_ERROR:
                    # self.update_result(result, f"Intente nuevamente más tarde:\n {entry['nombre']}", False)
                    self.update_result(
                        label1=f"Intente nuevamente más tarde: \n {entry['nombre']}",
                        c_label1='#fca5a5',
                        c_huella='#fca5a5',
                    )
                if result == CodeResponse.UNAUTHORIZED:
                    if self.label_auth is None:
                        self.label_auth = ctk.CTkLabel(self, text="Autenticar",
                                                       font=ctk.CTkFont(size=12, weight="bold"),
                                                       fg_color="red")
                        self.label_auth.configure(corner_radius=10)
                        self.label_auth.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)
                    # self.update_result(result, f"Marcando...\n {entry['nombre']}", False)
                    self.update_result(
                        label1=f"Error de autenticación",
                        c_label1='#fca5a5',
                        c_huella='#fca5a5',
                    )

                elif result == CodeResponse.ERROR:
                    # self.logger.save_log_error(f"Error con el servidor: {entry['nombre']} ")
                    # self.update_result(result,
                    #                    f"Error con el Servidor: {entry['nombre']} ", False)
                    self.update_result(
                        label1=f"Error con el servidor: {entry['nombre']}",
                        c_label1='#fca5a5',
                        c_huella='#fca5a5',
                    )

                break

        if not match_found:
            self.logger.save_log_error("Huella no identificada")
            # self.update_result(CodeResponse.ERROR, "Empleado no identificado", False)
            self.update_result(
                label1=f"Empleado no identificado",
                c_label1='#fca5a5',
                c_huella='#fca5a5',
            )
        imagen_ctk = ctk.CTkImage(light_image=self.filter_image, dark_image=self.filter_image, size=(200, 250))
        self.image_label = ctk.CTkLabel(self, image=imagen_ctk, text="", width=200, height=200, corner_radius=15)
        self.image_label.pack(padx=10, pady=10)

    def view_progress(self):
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=5)
        self.progress_bar.pack(side="top")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def update_result(self, label1: str, c_label1: str, c_huella: str, t_mark: str = None, c_mark: str = 'black'):

        self.label_result = ctk.CTkLabel(self, text=label1, text_color=c_label1)
        self.label_result.pack(padx=10, pady=10)
        self.filter_image = ImageOps.colorize(self.open_imagen, "black", c_huella)

        if t_mark is not None:
            self.label_mark = ctk.CTkLabel(self, text=t_mark,
                                           font=ctk.CTkFont(size=22, weight="bold", ),
                                           fg_color=c_mark, text_color='black')
            self.label_mark.configure(corner_radius=6)
            self.label_mark.pack(padx=15, pady=15, )
