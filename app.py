import customtkinter as ctk
from screens.reloj import Reloj


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.resizable(True, True)

        self.title("Tcontur Asistencia")
        self.iconbitmap("./assets/favicon.ico")

        self.view_clock()

    def view_clock(self):
        self.delete_pages()
        new_page = Reloj(self)
        new_page.pack(fill="both", expand=True)
        new_page.tkraise()

    def on_page(self, page):
        self.delete_pages()
        new_page = page(self)
        new_page.pack(fill="both", expand=True)
        new_page.tkraise()

    def delete_pages(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def view_clock(self):
        self.delete_pages()
        new_page = Reloj(self)
        new_page.pack(fill="both", expand=True)
        new_page.tkraise()

    def logout(self):
        self.auth.sign_out()
        self.check_auth()
