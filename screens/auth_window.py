import customtkinter as ctk


class AuthWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Ventana de Autenticación")
        self.geometry("300x200")

        self.label = ctk.CTkLabel(self, text="Introduce tu token:")
        self.label.pack(pady=20)

        self.token_entry = ctk.CTkEntry(self)
        self.token_entry.pack(pady=10)

        self.auth_button = ctk.CTkButton(self, text="Autenticar", command=self.authenticate)
        self.auth_button.pack(pady=20)

    def authenticate(self):
        token = self.token_entry.get()
        # Aquí puedes agregar la lógica para autenticar el token.
        # Si la autenticación es exitosa:
        self.master.set_token(token)
        self.destroy()
