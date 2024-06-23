import customtkinter as ctk
from controladores.device import Device
import threading
from PIL import Image
from servicios.auth import Auth


class AuthWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # self.title("Ventana de Autenticación")
        # self.geometry("300x200")
        self.auth = Auth()
        self.device = Device()
        # mantenemos esta ventana en primer plano
        # self.attributes("-topmost", True)
        # la centramos en base a la ventana principal
        # self.geometry(f"+{master.winfo_x() + 50}+{master.winfo_y() + 50}")
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="top", pady=2, fill="x")
        self.create_logo()
        self.create_widgets()
        self.button_volver = ctk.CTkButton(self, text="Volver", command=self.volver_a_reloj)
        self.button_volver.pack(padx=20, pady=20, side="bottom", anchor="e")

    def create_logo(self):
        # Un titulo , debe decir , Configuracion

        self.label_title = ctk.CTkLabel(self, text="Verificar Sistema", font=ctk.CTkFont(size=20, weight="bold"))
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

        # self.button_login = ctk.CTkButton(self, text="Ingresar", command=self.start_login_thread)
        # self.button_login.pack(pady=(20, 10))

        self.auth_button = ctk.CTkButton(self, text="Autenticar", command=self.login,
                                         fg_color="indigo", font=("Helvetica", 12))
        self.auth_button.pack(pady=20)

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
        # self.progress_bar.configure(height=5)
        # self.progress_bar.lift()
        # self.progress_bar.start()
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

    def authenticate(self):
        token = self.token_entry.get()
        # Aquí puedes agregar la lógica para autenticar el token.
        # Si la autenticación es exitosa:
        self.device.set_token(token)
        self.master.view_clock()
        self.destroy()
