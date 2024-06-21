import customtkinter as ctk
from controladores.device import Device


class AuthWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # self.title("Ventana de Autenticación")
        # self.geometry("300x200")
        self.device = Device()
        # mantenemos esta ventana en primer plano
        # self.attributes("-topmost", True)
        # la centramos en base a la ventana principal
        # self.geometry(f"+{master.winfo_x() + 50}+{master.winfo_y() + 50}")

        self.label = ctk.CTkLabel(self, text="Introduce tu token:")
        self.label.pack(pady=20)

        self.token_entry = ctk.CTkEntry(self)
        self.token_entry.pack(pady=10)

        self.auth_button = ctk.CTkButton(self, text="Autenticar", command=self.authenticate)
        self.auth_button.pack(pady=20)

    # def volver_a_reloj(self):
    #     # Llamar a la función en App para volver al Frame de Reloj
    #     self.master.view_clock()

    def authenticate(self):
        token = self.token_entry.get()
        # Aquí puedes agregar la lógica para autenticar el token.
        # Si la autenticación es exitosa:
        self.device.set_token(token)
        self.master.view_clock()
        self.destroy()
