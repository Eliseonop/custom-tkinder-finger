import customtkinter as ctk
import threading
from servicios.auth import Auth
from servicios.planilla_service import PlanillaService
from modelos.error_code import CodeResponse


class NoSubidas(ctk.CTkFrame):

    def __init__(self, master, auth: Auth):
        super().__init__(master)
        self.title_label = None
        self.upload_all_button = None
        self.progress_bar = None
        self.pack(fill="both", expand=True)
        self.auth = auth
        self.planilla_service = PlanillaService(self.auth)
        self.message_label = None
        self.initialize_ui_elements()
        self.load_marcaciones_offline()

    def initialize_ui_elements(self):
        self.progress_bar = ctk.CTkProgressBar(self, width=0, height=0)
        self.progress_bar.pack_forget()  # Oculta la barra de progreso al iniciar

        self.title_label = ctk.CTkLabel(self, text="Asistencias offline", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=20, padx=2, side="top")

        self.upload_all_button = ctk.CTkButton(self, text="Subir todas las asistencias",
                                               command=self.upload_all_marcaciones)
        self.upload_all_button.pack(pady=10, padx=2, side="top")

    def view_progress(self):
        self.progress_bar.pack(side="top")  # Muestra la barra de progreso
        self.progress_bar.configure(mode="indeterminate", height=5, width=400)
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()  # Oculta la barra de progreso

    def create_table(self, headers, marcaciones):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=400)
        self.scrollable_frame.pack(padx=20, pady=10)

        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5)

        for i, marcacion in enumerate(marcaciones):
            date_time = marcacion["hora"]
            empleado = marcacion["nombre"]
            date, time = date_time.split("T")
            time = time.split(".")[0]

            ctk.CTkLabel(self.scrollable_frame, text=date).grid(row=i + 1, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=time).grid(row=i + 1, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=empleado).grid(row=i + 1, column=2, padx=10, pady=5)

    def load_marcaciones_offline(self):
        self.view_progress()

        marcaciones = self.planilla_service.marcaciones_offline
        print(marcaciones)
        total = len(marcaciones)

        if total == 0:
            self.upload_all_button.pack_forget()  # Elimina el botón si no hay marcaciones
            self.stop_progress()
            self.display_message("No se encontraron marcaciones offline")
            return

        self.upload_all_button.pack(pady=10, padx=2, side="top")  # Muestra el botón si hay marcaciones
        headers = ["Fecha", "Hora", "Empleado"]
        self.create_table(headers, marcaciones)

        self.stop_progress()

    def clear_table(self):
        self.scrollable_frame.pack_forget()

    def display_message(self, message, pady=20, color="black"):
        if self.message_label:
            self.message_label.pack_forget()
        self.message_label = ctk.CTkLabel(self, text=message, text_color=color, font=("Arial", 14, "bold"))
        self.message_label.pack(padx=20, pady=pady)

    def upload_all_marcaciones(self):
        marcaciones = self.planilla_service.marcaciones_offline

        if not marcaciones:
            self.display_message("No hay asistencias para subir", color="red")
            return

        self.upload_all_button.pack_forget()  # Elimina el botón al iniciar la subida
        threading.Thread(target=self.upload_all_marcaciones_thread, args=(marcaciones,)).start()

    def upload_all_marcaciones_thread(self, marcaciones):
        self.view_progress()
        self.clear_table()

        for marcacion in marcaciones:
            empleado_id = marcacion["empleado"]
            date_time = marcacion["hora"]

            try:
                response = self.planilla_service.post_rectificar(empleado_id, date_time)

                if response == CodeResponse.SUCCESS:
                    print(f"Marcación de {marcacion['nombre']} subida correctamente")
                    self.planilla_service.delete_marcacion_offline(empleado_id, date_time)
                    self.display_message(f"Asistencia de {marcacion['nombre']} subida correctamente", color="green")
                elif response == CodeResponse.ERROR:
                    self.display_message(f"Error al subir asistencia de {marcacion['nombre']}", color="red")

            except Exception as e:
                self.display_message(f"Error al subir asistencia de {marcacion['nombre']}", color="red")

        self.display_message("Todas las asistencias se subieron correctamente", color="#a3e635")

        self.stop_progress()
        # self.load_marcaciones_offline()
