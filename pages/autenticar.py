import customtkinter as ctk
from tkinter import messagebox
from servicios.auth import Auth
from PIL import Image
import threading
from screens.auth_window import AuthWindow


class Autenticar(ctk.CTkFrame):
    def __init__(self, parent, auth: Auth):
        super().__init__(parent)
        print("Autenticar")
        self.auth = auth
        self.app = parent
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=0)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.pack(side="top", fill="x")
        # self.progress_bar.pack_forget()
        self.create_logo()
        self.create_widgets()
        self.create_scale()
        self.button_volver = ctk.CTkButton(self, text="Volver", command=self.app.volver_a_reloj)
        self.button_volver.pack(padx=20, pady=20, side="bottom", anchor="e")

    def create_scale(self):
        frame_scale = ctk.CTkFrame(self)
        frame_scale.pack(pady=(20, 20), padx=(20, 20), side="bottom", anchor="w")
        self.appearance_mode_label = ctk.CTkLabel(frame_scale, text="Tema:", anchor="w")
        self.appearance_mode_label.pack(side="left", padx=20)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(frame_scale,
                                                             values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event,
                                                             variable=ctk.StringVar(value="System"))
        self.appearance_mode_optionemenu.pack(side="left", padx=20)

        self.scaling_label = ctk.CTkLabel(frame_scale, text="Escala UI :", anchor="w")
        self.scaling_label.pack(side="left", padx=20)
        self.scaling_optionemenu = ctk.CTkOptionMenu(frame_scale,
                                                     values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event,
                                                     variable=ctk.StringVar(value="100%")
                                                     )
        self.scaling_optionemenu.pack(side="left", padx=20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def volver_a_reloj(self):
        self.app.view_clock()

    def create_logo(self):
        # Un titulo , debe decir , Configuracion

        self.label_title = ctk.CTkLabel(self, text="Configuración", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(20, 20))

        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(50, 50))
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="", font=ctk.CTkFont(size=20, weight="bold"),
                                       compound="left")
        self.logo_label.pack(pady=20)

    def create_widgets(self):
        # Frame para username
        frame_username = ctk.CTkFrame(self)
        frame_username.pack(pady=(20, 20), padx=(20, 20))

        self.label_username = ctk.CTkLabel(frame_username, text="Usuario")
        self.label_username.pack()

        self.entry_username = ctk.CTkEntry(frame_username)
        self.entry_username.pack(pady=(5, 10), padx=(20, 20))

        frame_password = ctk.CTkFrame(self)
        frame_password.pack(pady=(10, 10), padx=(20, 20))

        self.label_password = ctk.CTkLabel(frame_password, text="Contraseña")
        self.label_password.pack()

        self.entry_password = ctk.CTkEntry(frame_password, show="*")
        self.entry_password.pack(pady=(5, 10), padx=(20, 20))

        self.button_login = ctk.CTkButton(self, text="Ingresar", command=self.start_login_thread)
        self.button_login.pack(pady=(20, 10))

    def start_login_thread(self):
        # Inicia un nuevo hilo para el proceso de login
        login_thread = threading.Thread(target=self.login)
        login_thread.start()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # self.progress_bar.pack(side="top", fill="x")
        # self.progress_bar.configure(mode="indeterminate")

        # self.progress_bar.pack(side="top", fill="x")
        self.progress_bar.configure(height=5)
        self.progress_bar.lift()
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
