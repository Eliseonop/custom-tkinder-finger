import customtkinter as ctk
from controladores.controlador_principal import ControladorPrincipal


class Dispositivo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
