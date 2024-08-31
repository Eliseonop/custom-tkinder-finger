import customtkinter as ctk
from tkinter import StringVar, messagebox
from servicios.planilla_service import PlanillaService
from servicios.auth import Auth
import threading
from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image
from pyzkfp import ZKFP2
from tkinter import messagebox
import time


class SubirTemplate(ctk.CTkScrollableFrame):
    def __init__(self, master, auth: Auth):
        super().__init__(master)
        self.dis_message = None
        self.thread_fing = None
        self.pack(fill="both", expand=True)
        # self.title_window()
        self.initialize_ui_elements()
        self.initialize_fingerprint_device()
        self.initialize_services(auth)
        print("Inicializando vista de subir template")
        self.lista_empleados = []
        self.filtered_empleados = []
        self.selected_template = None
        self.selected_empleado = None
        self.whileValue = False
        self.frame_action_cancel = None
        self.frame_action = None
        self.scroll_height = 450
        self.load_empleados()

    def destroy(self):
        self.whileValue = False

        print("Destruyendo vista de subir template")
        super().destroy()

    def initialize_ui_elements(self):
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="top", pady=2, fill="x")
        self.title_label = ctk.CTkLabel(self, text="Registro de Huella", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=2, padx=2, side="top")
        self.image_label = None
        self.fingerprint_message_label = None
        self.frame_title_finger = None

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

    def initialize_services(self, auth):
        # auth = Auth()
        self.planilla_service = PlanillaService(auth)

    def load_empleados(self):
        threading.Thread(target=self.load_empleados_thread).start()

    def load_empleados_thread(self):
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        if self.planilla_service.obtener_empleados():
            # sleep(1)
            print(self.planilla_service.empleados)
            self.lista_empleados = self.planilla_service.empleados

            self.filtered_empleados = self.lista_empleados
            self.initialize_main_template()
            # self.initialize_finger_template()
        else:
            print('No se han podido cargar las huellas')
            self.display_message("No se han podido cargar los empleados", "red")

        self.progress_bar.pack_forget()

    def initialize_main_template(self):

        self.frame_general_table = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_general_table.pack(pady=10)

        self.frame_search = ctk.CTkFrame(self.frame_general_table)
        self.frame_search.pack(pady=2, padx=20)

        self.label_buscar = ctk.CTkLabel(self.frame_search, text="Buscar Empleado")
        self.label_buscar.pack(padx=20, pady=2)

        self.var = StringVar()
        self.entry = ctk.CTkEntry(self.frame_search, textvariable=self.var)
        self.entry.pack(padx=20, pady=10)
        self.entry.bind('<KeyRelease>', self.check_autocomplete)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_general_table, width=860, height=self.scroll_height)
        self.scrollable_frame.pack(padx=20, pady=5)

        self.create_employee_table()

    def create_employee_table(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Nombre", "Tiene Huella", "Acciones"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        for i, empleado in enumerate(self.filtered_empleados, start=1):
            label = ctk.CTkLabel(self.scrollable_frame, text=empleado['nombre'], width=300)
            label.grid(row=i, column=0, padx=5, pady=5)

            # texto de tiene huella o no si empleado['huella'] es None o el string vacío
            next_label = "No tiene huella" if not empleado['huella'] else "Tiene huella"

            label = ctk.CTkLabel(self.scrollable_frame, text=next_label, width=300,
                                 text_color="green" if empleado['huella'] else "red")
            label.grid(row=i, column=1, padx=5, pady=5)

            register_button = ctk.CTkButton(self.scrollable_frame, text="Registrar Huella",
                                            command=lambda e=empleado: self.capture_fingerprint(e))
            register_button.grid(row=i, column=2, padx=5, pady=5)

    def initialize_finger_template(self):
        self.frame_action = ctk.CTkFrame(self)
        self.frame_action.pack(pady=20)

        self.capture_button = ctk.CTkButton(self.frame_action, text="Reintentar", command=self.capture_fingerprint,
                                            fg_color="#57534e"
                                            )
        self.capture_button.pack(padx=20, pady=10, side="left")

        self.submit_button = ctk.CTkButton(self.frame_action, text="Registrar", command=self.submit_form,

                                           fg_color="indigo")

        self.submit_button.pack(padx=20, pady=10, side="left")

    def capture_fingerprint(self, empleado=None):
        self.clear_display_message()
        print("Capturando huella")
        print(self.selected_empleado)
        print(threading.active_count())
        self.whileValue = False

        if self.thread_fing and self.thread_fing.is_alive():
            self.whileValue = False
            self.thread_fing.join()

        # cancelar el hilo de captura de huella
        if self.frame_general_table:
            self.frame_general_table.pack_forget()

            self.whileValue = False

        if self.frame_action_cancel is not None:
            self.frame_action_cancel.pack_forget()

        if self.frame_action:
            self.frame_action.pack_forget()

        if empleado:
            self.selected_empleado = empleado

        self.hide_fingerprint_message()
        self.show_fingerprint_message()
        self.thread_fing = threading.Thread(target=self.thread_capture_fingerprint).start()

    def cancelar(self):
        self.selected_empleado = None
        self.selected_template = None
        # self.zkfp2.DBFree()
        if self.thread_fing and self.thread_fing.is_alive():
            self.whileValue = False
            self.thread_fing.join()

        self.whileValue = False
        if self.image_label:
            self.image_label.pack_forget()
            self.image_label = None
        if self.frame_action_cancel is not None:
            self.frame_action_cancel.pack_forget()
            self.frame_action_cancel = None
        if self.frame_action is not None:
            self.frame_action.pack_forget()
            self.frame_action = None

        self.hide_fingerprint_message()
        self.show_table()

    def thread_capture_fingerprint(self):
        try:
            self.whileValue = True
            regTemp, imgs = self.capturar_huella_fucion(3)
            if regTemp and imgs:
                self.selected_template = b64encode(bytes(regTemp)).decode()
                self.write_img(imgs[0])
                self.initialize_finger_template()
                if self.fingerprint_message_label:
                    self.fingerprint_message_label.pack_forget()
        except Exception as e:
            print(f"Error al capturar huella: {e}")

    def capturar_huella_fucion(self, veces):
        print('inciando captura')

        self.label_count = ctk.CTkLabel(self.frame_title_finger, text=f'',
                                        font=("Arial", 17, "bold"))
        self.progress_count = ctk.CTkProgressBar(self.frame_title_finger, width=200, height=5, mode="determinate")
        try:
            templates, imgs = [], []

            for i in range(veces):

                print('captura', i)
                self.progress_count.set((i + 1) / veces)
                self.progress_count.pack(pady=2)
                self.label_count.configure(text=f'Esperando Huella {i + 1} de {veces}', text_color="green")
                self.label_count.pack(pady=10, padx=10)

                while self.whileValue:
                    capture = self.zkfp2.AcquireFingerprint()

                    if capture:
                        print('Huella dactilar capturada')
                        tmp, img = capture

                        templates.append(tmp)
                        imgs.append(capture[1])

                        if (i + 1) == 3:
                            print('Huella capturada')
                            self.label_count.configure(text="Huella capturada", text_color="green")
                            self.progress_count.stop()
                            self.progress_count.pack_forget()

                        break
            regTemp, regTempLen = self.zkfp2.DBMerge(*templates)
            return regTemp, imgs
        except Exception as e:
            print(f"Error al capturar huella: {e}")

    def acquire_fingerprint_data(self):
        templates, imgs = [], []

        self.whileValue = True

        while self.whileValue:
            capture = self.zkfp2.AcquireFingerprint()
            if self.whileValue is False:
                break
            if capture:
                print('Huella dactilar capturada')
                templates.append(capture[0])
                imgs.append(capture[1])
                self.whileValue = False
                break
        return templates, imgs

    def show_fingerprint_message(self):

        self.frame_title_finger = ctk.CTkFrame(self)
        self.frame_title_finger.pack(pady=10)
        title = f"Registrar huella de {self.selected_empleado['nombre']}"
        self.label_title_finger = ctk.CTkLabel(self.frame_title_finger, text=title, font=("Arial", 17, "bold"))
        self.label_title_finger.pack(pady=10, padx=10)

        self.frame_action_cancel = ctk.CTkFrame(self)
        self.frame_action_cancel.pack(pady=5, padx=5)
        self.cancel_button = ctk.CTkButton(self.frame_action_cancel, text="Cancelar", command=self.cancelar,
                                           fg_color="red")
        self.cancel_button.pack(padx=20, pady=10, side="left")

        if self.image_label:
            self.image_label.pack_forget()

        self.fingerprint_message_label = ctk.CTkLabel(self, text=" ¡ Por favor coloque su dedo en el lector ... !",
                                                      font=("Arial", 18, "bold"))

        self.fingerprint_message_label.pack(pady=10, padx=10 * 2)
        self.update()

    def hide_fingerprint_message(self):
        if self.fingerprint_message_label:
            self.fingerprint_message_label.pack_forget()
        if self.frame_title_finger:
            self.frame_title_finger.pack_forget()

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

    def display_message(self, message, t_color: str):
        self.dis_message = ctk.CTkLabel(self, text=message, text_color=t_color)
        self.dis_message.pack(padx=20, pady=10, )

    def clear_display_message(self):
        if self.dis_message:
            self.dis_message.pack_forget()

    def update_submit_button_state(self):
        if self.selected_empleado and self.selected_template:
            self.capture_button.configure(state="normal")
        else:
            self.capture_button.configure(state="disabled")

    def submit_form(self):
        if not self.selected_empleado:
            print("No se ha seleccionado ningún empleado")
            return

        threading.Thread(target=self.upload_finger, args=(self.selected_empleado['id'], self.selected_template)).start()

    def upload_finger(self, empleado, huella):
        # print("Enviando datos:", datos)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.start()
        self.progress_bar.pack(side="top", pady=2)

        try:
            response, json = self.planilla_service.upload_huella(empleado, huella)

            if response:
                self.progress_bar.stop()
                self.progress_bar.pack_forget()
                self.display_message("Huella subida correctamente", "green")
                self.cancelar()

            else:
                # print('ojo')
                self.display_message(json, 'red')
                messagebox.showerror("Error", json)
                # ctk.CTkToplevel(title="Error", message=json, icon="warning")
                self.progress_bar.stop()
                self.progress_bar.pack_forget()

        except Exception as e:
            print(f"Error al subir la huella: {e}")
            messagebox.showerror("Error", 'Error del Servidor')

            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.display_message("Error al subir la huella", "red")
            # self.cancelar()

    def check_autocomplete(self, event):
        typed = self.var.get().lower()
        self.filtered_empleados = [empleado for empleado in self.lista_empleados if typed in empleado['nombre'].lower()]
        self.create_employee_table()

    def show_table(self):
        if self.frame_general_table:
            self.frame_general_table.pack(padx=20, pady=10)
