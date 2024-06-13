import customtkinter as ctk
from controladores.device import Device


class Dispositivo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
