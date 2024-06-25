import customtkinter as ctk
from servicios.auth import Auth
from vistas.main_config import MainConfig
from screens.autenticar_config import AutenticarConfig
import threading


class Configuracion(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # self.join_threads()
        self.auth = Auth()

        self.check_auth()

    def join_threads(self):
        for thread in threading.enumerate():
            if thread is not threading.current_thread():
                thread.join()
                print(f"Deteniendo hilo {thread}")

    def volver_a_reloj(self):
        # Llamar a la función en App para volver al Frame de Reloj
        self.master.view_clock()

    def check_auth(self):
        print("Checking auth")
        self.delete_pages()
        if self.auth.token:
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
