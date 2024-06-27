import customtkinter as ctk
import threading
from PIL import Image
from servicios.auth import Auth
from servicios.empresa_service import EmpresaService


class Auth_Reloj(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.auth = Auth()
        self.empresa_service = EmpresaService()
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=0)
        self.progress_bar.pack(side="top", pady=2, fill="x")

        self.create_logo()
        self.create_widgets()
        self.button_volver = ctk.CTkButton(self, text="Volver", command=self.volver_a_reloj)
        self.button_volver.pack(padx=20, pady=20, side="bottom", anchor="e")

        # Verificar campos inicial
        self.empresa_service.view_message_if_not_empresa()
        self.check_fields()

    def create_logo(self):
        # Un titulo , debe decir , Configuracion
        self.label_title = ctk.CTkLabel(self, text="Verificar Sistema", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(20, 20))

        self.logo_image = ctk.CTkImage(Image.open("./assets/logo.png"), size=(50, 50))
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
        self.entry_username.bind("<KeyRelease>", lambda event: self.check_fields())

        frame_password = ctk.CTkFrame(self)
        frame_password.pack(pady=(10, 10), padx=(20, 20))

        self.label_password = ctk.CTkLabel(frame_password, text="Contraseña")
        self.label_password.pack()

        self.entry_password = ctk.CTkEntry(frame_password, show="*")
        self.entry_password.pack(pady=(5, 10), padx=(20, 20))
        self.entry_password.bind("<KeyRelease>", lambda event: self.check_fields())

        self.auth_button = ctk.CTkButton(self, text="Autenticar", command=self.login,
                                         fg_color="indigo", font=("Helvetica", 12))
        self.auth_button.pack(pady=20)

    def check_fields(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        empresa_storage = self.empresa_service.get_empresa_storage()
        print(empresa_storage)
        if username and password and empresa_storage:
            self.auth_button.configure(state="normal")
        else:
            self.auth_button.configure(state="disabled")

    def start_login_thread(self):
        login_thread = threading.Thread(target=self.login)
        login_thread.start()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.progress_bar.configure(height=5)
        self.progress_bar.pack(side="top", fill="x")
        self.progress_bar.lift()
        self.progress_bar.start()
        try:
            success = self.auth.sign_in(username, password)
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            if success:
                print("Login successful")
                self.volver_a_reloj()
                self.destroy()
                # Navegar a la página principal
            else:
                # messagebox.showerror("Error", "Invalid credentials")
                print("Invalid credentials")
        except Exception as e:
            self.progress_bar.stop()
            # messagebox.showerror("Error", str(e))

    def volver_a_reloj(self):
        # Llamar a la función en App para volver al Frame de Reloj
        self.master.view_clock()
