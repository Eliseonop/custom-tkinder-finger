import customtkinter as ctk
from varios.vistas.body import Body
from varios.vistas.sidebar import Sidebar
from varios.vistas.vista1 import Vista1


class VistaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x640")
        self.resizable(False, False)
        self.title("Finger Print Tcontur")

        self.create_sidebar()
        self.create_body()

        self.controlador = None

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
            {"name": "Vista 1", "vista": Vista1},
            # {"name": "Vista 2", "vista": Vista2},  # Ajusta el nombre y la vista según tus necesidades
            # {"name": "Vista 3", "vista": Vista3}
        ]

        self.sidebar = Sidebar(self, self.change_appearance_mode_event,
                               self.change_scaling_event,
                               self.on_page, button_info_list)
        self.sidebar.pack(side="left", fill="y")  # Llenar verticalmente el sidebar

    def create_body(self):
        self.body = Body(self)
        self.body.pack(fill="both", expand=True)  # Para que el body se expanda y ocupe todo el espacio disponible

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self, ruta):
        if self.controlador:
            self.controlador.mostrar_vista(ruta)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def set_controlador(self, controlador):
        self.controlador = controlador
