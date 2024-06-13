import customtkinter as ctk
from servicios.auth import Auth
from vistas.vista_principal import VistaPrincipal
from pages.autenticar import Autenticar


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x640")
        self.resizable(False, False)
        self.title("Tcontur Asistencia")

        # self.controlador = ControladorPrincipal(self)
        self.auth = Auth()
        self.check_auth()

    def check_auth(self):
        print("Checking auth")
        self.delete_pages()
        if self.auth.get_access_token():
            print("Access token found")
            new_page = VistaPrincipal(self, self.auth, self.logout)
            new_page.pack(fill="both", expand=True)
            new_page.tkraise()
        else:
            print("Access token not found")
            new_page = Autenticar(self, self.auth)
            new_page.pack(fill="both", expand=True)
            new_page.tkraise()

    # def on_page(self, page):
    #     self.delete_pages()
    #     new_page = page(self, self.auth)
    #
    #     new_page.pack(fill="both", expand=True)
    #
    #     new_page.tkraise()

    def delete_pages(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def logout(self):
        self.auth.sign_out()
        self.check_auth()
