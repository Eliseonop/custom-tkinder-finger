import customtkinter as ctk
from servicios.auth import Auth
from vistas.main_config import MainConfig
from screens.autenticar_config import AutenticarConfig


class CheckAuth(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x640")
        self.resizable(True, True)

        self.title("Tcontur Asistencia")
        self.iconbitmap("favicon.ico")

        # self.controlador = ControladorPrincipal(self)
        self.auth = Auth()
        self.check_auth()

    def check_auth(self):
        print("Checking auth")
        self.delete_pages()
        if self.auth.token is not None:
            print("Access token found")
            new_page = MainConfig(self, self.auth, self.logout)
            new_page.pack(fill="both", expand=True)
            new_page.tkraise()
        else:
            print("Access token not found")
            new_page = AutenticarConfig(self, self.auth)
            new_page.pack(fill="both", expand=True)
            new_page.tkraise()

    def delete_pages(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def logout(self):
        self.auth.sign_out()
        self.check_auth()
