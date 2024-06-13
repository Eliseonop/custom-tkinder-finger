import customtkinter as ctk
from controladores.controlador_principal import ControladorPrincipal
from vistas.subirtemplate import SubirTemplate
from vistas.marcar import Marcar
from vistas.dispositivo import Dispositivo
from utils.sidebar import Sidebar
from utils.body import Body
from servicios.auth import Auth


class VistaPrincipal(ctk.CTkFrame):
    def __init__(self, master, auth: Auth, logout):
        super().__init__(master)
        # self.geometry("1024x640")
        # self.resizable(False, False)
        # self.title("Tcontur Asistencia")
        self.logout = logout
        self.master = master
        self.auth = auth
        self.create_sidebar()
        self.create_body()

        # self.controlador = ControladorPrincipal()
        self.on_page(SubirTemplate)

    def salir(self):
        self.logout()

    def on_page(self, page):
        self.delete_pages()
        new_page = page(self.body)

        new_page.pack(fill="both", expand=True)

        new_page.tkraise()

    def delete_pages(self):
        for widget in self.body.winfo_children():
            widget.pack_forget()  # Quitamos todos los widgets del body

    def create_sidebar(self):
        button_info_list = [
            {"name": "Registrar", "vista": SubirTemplate},
            {"name": "Autenticar", "vista": Marcar},  # Ajusta el nombre y la vista según tus necesidades
            {"name": "Dispositivo", "vista": Dispositivo}
        ]

        self.sidebar = Sidebar(self, self.change_appearance_mode_event,
                               self.change_scaling_event,
                               self.on_page, button_info_list, self.salir)
        self.sidebar.pack(side="left", fill="y", )  # Llenar verticalmente el sidebar

    def create_body(self):
        self.body = Body(self)
        self.body.pack(fill="both", expand=True)  # Para que el body se expanda y ocupe todo el espacio disponible

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
