import customtkinter as ctk
# from vistas.vista_principal import VistaPrincipal
from app import App

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")

app = App()
app.mainloop()
