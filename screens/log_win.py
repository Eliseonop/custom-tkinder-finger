import logging
from tkinter import messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class LogWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("600x600")
        self.title("Registro de Eventos")

        self.frame_scroll = ctk.CTkScrollableFrame(self)
        self.frame_scroll.pack(fill="both", expand=True)

        self.frame = ctk.CTkFrame(self.frame_scroll)

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.frame.pack(fill="both", expand=True)
        self.load_logs()

    def load_logs(self):
        try:
            with open("app.log", "r") as file:
                logs_data = file.readlines()

                for index, log in enumerate(logs_data):
                    log_parts = log.split(' - ')
                    print(log_parts)
                    if len(log_parts) == 3:  # Asegurar que el log tenga el formato esperado
                        hora_label = ctk.CTkLabel(self.frame, text=log_parts[0])
                        hora_label.grid(row=index, column=0, sticky="w", padx=10)

                        data_label = ctk.CTkLabel(self.frame, text=log_parts[1])
                        data_label.grid(row=index, column=1, sticky="e", padx=10)

                        message_label = ctk.CTkLabel(self.frame, text=log_parts[2])
                        message_label.grid(row=index, column=2, sticky="e", padx=10)

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al cargar los logs: {e}",
                icon="warning",
            )
