import customtkinter as ctk
# from vistas.vista_principal import VistaPrincipal
from app import App
from utils.storage import Storage
from dotenv import load_dotenv

load_dotenv()

storage = Storage()

appearance_mode = storage.load('appearance_mode')
scaling = storage.load('scaling')
print(appearance_mode, scaling)

ctk.set_appearance_mode(appearance_mode if appearance_mode else 'system')
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(scaling if scaling else 1.0)
app = App()

app.mainloop()
