import json
from tkinter import messagebox
import customtkinter as ctk


class LogWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("600x600")
        self.title("Registro de Eventos")
        self.frame = ctk.CTkFrame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.pack(fill="both", expand=True)
        self.load_logs()

    def load_logs(self):
        try:
            with open("log.json", "r") as file:
                logs = file.readlines()
                logs_data = [json.loads(log.strip()) for log in logs]

                for index, log in enumerate(logs_data):
                    hora_label = ctk.CTkLabel(self.frame, text=log['hora'])
                    hora_label.grid(row=index, column=0, sticky="w", padx=10)

                    data_label = ctk.CTkLabel(self.frame, text=log['data'])
                    data_label.grid(row=index, column=1, sticky="e", padx=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los logs: {e}")
