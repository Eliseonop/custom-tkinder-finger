import customtkinter as ctk
from controladores.device import Device
from vistas.subirtemplate import SubirTemplate
from vistas.servidor import Servidor
from vistas.dispositivo import Dispositivo
from utils.sidebar import Sidebar
from utils.body import Body
from servicios.auth import Auth


class Menu(ctk.CTkFrame):
    def __init__(self, master, auth: Auth, on_page_callback):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        # self.geometry("1024x640")
        # self.resizable(False, False)
        # self.title("Tcontur Asistencia")
        # self.logout = logout
        self.master = master
        self.auth = auth
        # self.create_sidebar()
        # self.create_body()

        # self.controlador = ControladorPrincipal()
        # self.on_page(SubirTemplate)
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, padx=20, pady=20)
        self.buttons = [
            {"name": "Registrar", "vista": SubirTemplate},
            {"name": "Servidor", "vista": Servidor},  # Ajusta el nombre y la vista según tus necesidades
            # {"name": "Dispositivo", "vista": Dispositivo}
        ]
        self.create_buttons(on_page_callback)

    def create_buttons(self, on_page_callback):

        for i in range(2):
            self.container.grid_columnconfigure(i, weight=1)
            self.container.grid_rowconfigure(i, weight=1)

            # Crear y colocar los botones a partir de la lista
        for index, button_info in enumerate(self.buttons):
            name = button_info["name"]
            vista = button_info["vista"]
            row = index // 2
            col = index % 2
            button = ctk.CTkButton(self.container, text=name, command=lambda v=vista: on_page_callback(v))
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

    def salir(self):
        self.logout()

    # def on_page(self, page):
    #     self.delete_pages()
    #     new_page = page(self.body)
    #
    #     new_page.pack(fill="both", expand=True)
    #
    #     new_page.tkraise()
    #
    # def delete_pages(self):
    #     for widget in self.body.winfo_children():
    #         widget.pack_forget()  # Quitamos todos los widgets del body
    #
    # def create_sidebar(self):
    #     button_info_list = [
    #         {"name": "Registrar", "vista": SubirTemplate},
    #         {"name": "Servidor", "vista": Servidor},  # Ajusta el nombre y la vista según tus necesidades
    #         {"name": "Dispositivo", "vista": Dispositivo}
    #     ]
    #
    #     self.sidebar = Sidebar(self, self.change_appearance_mode_event,
    #                            self.change_scaling_event,
    #                            self.on_page, button_info_list, self.salir)
    #     self.sidebar.pack(side="top", fill="x", )  # Llenar verticalmente el sidebar
    #
    # def create_body(self):
    #     self.body = Body(self)
    #     self.body.pack(fill="both", expand=True)  # Para que el body se expanda y ocupe todo el espacio disponible
    #
    # def change_appearance_mode_event(self, new_appearance_mode: str):
    #     ctk.set_appearance_mode(new_appearance_mode)
    #
    # def change_scaling_event(self, new_scaling: str):
    #     new_scaling_float = int(new_scaling.replace("%", "")) / 100
    #     ctk.set_widget_scaling(new_scaling_float)
