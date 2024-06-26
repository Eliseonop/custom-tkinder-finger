import customtkinter as ctk
import threading
from servicios.auth import Auth
from servicios.planilla_service import PlanillaService
import time


class NoSubidas(ctk.CTkFrame):

    def __init__(self, master, auth: Auth):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.auth = auth
        self.planilla_service = PlanillaService(self.auth)
        self.message_label = None
        self.buttons = []

        # self.create_table()
        threading.Thread(target=self.load_marcaciones_offline, daemon=True).start()

    def view_progress(self):
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=5)
        self.progress_bar.pack(side="top")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def create_table(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=400)
        self.scrollable_frame.pack(padx=20, pady=10)

    def load_marcaciones_offline(self):
        self.view_progress()
        # self.create_table()
        # self.clear_table()

        marcaciones = self.planilla_service.marcaciones_offline
        print(marcaciones)
        total = len(marcaciones)

        if total == 0:
            self.stop_progress()

            self.display_message("No se encontraron marcaciones offline")
            return
        headers = ["Fecha", "Hora", "Empleado", "Acciones"]
        # Crear encabezados de la tabla

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=400)
        self.scrollable_frame.pack(padx=20, pady=10)

        for col, header in enumerate(headers):
            self.scrollable_frame.grid_columnconfigure(0, weight=1)

            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5)

        for i, marcacion in enumerate(marcaciones):
            date_time = marcacion["hora"]
            empleado = marcacion["nombre"]
            date, time = date_time.split("T")
            time = time.split(".")[0]

            self.scrollable_frame.grid_columnconfigure(i + 1, weight=1)

            ctk.CTkLabel(self.scrollable_frame, text=date).grid(row=i + 1, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=time).grid(row=i + 1, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=empleado).grid(row=i + 1, column=2, padx=10, pady=5)

            rectificar_button = ctk.CTkButton(
                self.scrollable_frame, text="Rectificar",
                command=lambda m=marcacion: self.rectificar_marcacion(m)
            )
            rectificar_button.grid(row=i + 1, column=3, padx=10, pady=5)
            self.buttons.append(rectificar_button)

        self.stop_progress()

    def clear_table(self):
        self.scrollable_frame.pack_forget()

    def display_message(self, message, pady=20, color="black"):
        if self.message_label:
            self.message_label.pack_forget()
        self.message_label = ctk.CTkLabel(self, text=message, text_color=color, font=("Arial", 12, "bold"))
        self.message_label.pack(padx=20, pady=pady)

    def rectificar_marcacion(self, marcacion):
        # self.toggle_buttons(False)
        self.clear_table()

        empleado_id = marcacion["empleado"]
        date_time = marcacion["hora"]
        threading.Thread(target=self.upload_marcacion, args=(empleado_id, date_time)).start()

    def upload_marcacion(self, empleado_id, hora):
        self.view_progress()
        # self.display_message("Subiendo marcación...")

        try:
            response = self.planilla_service.post_rectificar(empleado_id, hora)

            if response:
                self.display_message("Asistencia rectificada correctamente", color="green")
                self.planilla_service.delete_marcacion_offline(empleado_id, hora)
                self.stop_progress()
                self.load_marcaciones_offline()
            else:
                self.stop_progress()
                self.display_message("Error al rectificada asistencia", color="red")
                self.load_marcaciones_offline()

        except Exception as e:
            self.display_message("Error al rectificada asistencia", color="red")
            self.stop_progress()
            self.load_marcaciones_offline()

        # finally:
        #     # self.toggle_buttons(True)

    # def reload_table(self):
    #     self.clear_table()
    #     self.load_marcaciones_offline()

    # def toggle_buttons(self, state):
    #     for button in self.buttons:
    #         button.configure(state=("normal" if state else "disabled"))
