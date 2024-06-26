import customtkinter as ctk
from tkinter import messagebox
from servicios.auth import Auth
from PIL import Image
import threading


class Autenticar(ctk.CTkFrame):
    def __init__(self, parent, auth: Auth):
        super().__init__(parent)
        print("Autenticar")
        self.auth = auth
        self.app = parent
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)

        self.create_logo()
        self.create_widgets()

        self.button_volver = ctk.CTkButton(self, text="Volver", command=self.app.volver_a_reloj)
        self.button_volver.pack(pady=(20, 10))

    def volver_a_reloj(self):
        self.app.view_clock()

    def create_logo(self):
        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(50, 50))
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="", font=ctk.CTkFont(size=20, weight="bold"),
                                       compound="left")
        self.logo_label.pack(pady=20)

    def create_widgets(self):
        # Frame para username
        frame_username = ctk.CTkFrame(self)
        frame_username.pack(pady=(20, 0))

        self.label_username = ctk.CTkLabel(frame_username, text="Usuario")
        self.label_username.pack()

        self.entry_username = ctk.CTkEntry(frame_username)
        self.entry_username.pack(pady=(5, 10))

        frame_password = ctk.CTkFrame(self)
        frame_password.pack(pady=(10, 0))

        self.label_password = ctk.CTkLabel(frame_password, text="Contraseña")
        self.label_password.pack()

        self.entry_password = ctk.CTkEntry(frame_password, show="*")
        self.entry_password.pack(pady=(5, 10))

        self.button_login = ctk.CTkButton(self, text="Ingresar", command=self.start_login_thread)
        self.button_login.pack(pady=(20, 10))

    def start_login_thread(self):
        # Inicia un nuevo hilo para el proceso de login
        login_thread = threading.Thread(target=self.login)
        login_thread.start()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.progress_bar.pack(side="bottom", fill="x")

        self.progress_bar.start()
        try:
            success = self.auth.sign_in(username, password)
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            if success:
                self.app.check_auth()  # Navegar a la página principal
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            self.progress_bar.stop()
            messagebox.showerror("Error", str(e))
