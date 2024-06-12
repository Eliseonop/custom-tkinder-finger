import customtkinter as ctk
from vistas.vista_principal import VistaPrincipal
from controladores.controlador_principal import ControladorPrincipal

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")

controlador = ControladorPrincipal()
app = VistaPrincipal(controlador)
# app.set_controlador(controlador)
app.mainloop()
