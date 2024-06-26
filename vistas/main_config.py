import customtkinter as ctk
from controladores.device import Device
from vistas.subirtemplate import SubirTemplate
from vistas.servidor import Servidor
# from vistas.dispositivo import Dispositivo
# from utils.sidebar import Sidebar
# from utils.body import Body
from servicios.auth import Auth
from vistas.no_subidas import NoSubidas
from PIL import Image
from utils.storage import Storage


class MainConfig(ctk.CTkFrame):
    def __init__(self, master, auth: Auth, logout):
        super().__init__(master)

        self.logout = logout
        self.master = master
        self.auth = auth
        self.storage = Storage()

        self.buttons = [
            {"name": "Registrar", "vista": SubirTemplate, "icon": "./assets/user_add.png"},
            {"name": "Servidor", "vista": Servidor, "icon": "./assets/server.png"},
            {"name": "Asistencias offline", "vista": NoSubidas, "icon": "./assets/error.png"}

        ]

        self.create_main()
        self.view_menu()

        # self.on_page(SubirTemplate)

    def create_main(self):
        subframe = ctk.CTkFrame(self)
        subframe.configure(height=50)

        subframe.pack(fill="x", side="top")

        self.logo_image = ctk.CTkImage(Image.open("./assets/logo.png"), size=(50, 50))
        self.logo_label = ctk.CTkLabel(subframe, image=self.logo_image, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"), compound="left")
        self.logo_label.pack(side="left", padx=20, pady=(20, 10), anchor="center")

        self.label_title = ctk.CTkLabel(subframe, text="Tcontur Asistencia", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_title.pack(side="left", padx=20, pady=(20, 10), anchor="center")

        self.boton_autenticar = ctk.CTkButton(subframe, text="Cerrar sesión", command=self.logout)

        self.boton_autenticar.pack(side="right", padx=20, pady=(20, 10))

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True)

    def view_menu(self):
        self.delete_pages()
        self.container = ctk.CTkFrame(self.main, )
        self.container.pack(expand=True, fill="both")

        for i in range(self.buttons.__len__()):
            self.container.grid_columnconfigure(i, weight=1)
            self.container.grid_rowconfigure(i, weight=1)

        # Crear y colocar los botones a partir de la lista
        for index, button_info in enumerate(self.buttons):
            name = button_info["name"]
            vista = button_info["vista"]
            icon = button_info["icon"]
            row = index // 2
            col = index % 2

            subframe = ctk.CTkFrame(self.container)
            subframe.grid(row=row, column=col, padx=30, pady=30)
            icon = ctk.CTkImage(Image.open(icon), size=(50, 50))
            icon_label = ctk.CTkLabel(subframe, image=icon, text="",
                                      font=ctk.CTkFont(size=20, weight="bold"), compound="left")
            icon_label.pack(side="left", padx=20, pady=(20, 10))

            button = ctk.CTkButton(subframe, text=name, command=lambda v=vista: self.on_page(v),
                                   font=("Helvetica", 22))
            button.pack(padx=20, pady=(20, 20))
            # button.grid(row=row, column=col, padx=10, pady=10)

        # def salir(self):
        #     self.logout()

    def on_page(self, page):
        self.delete_pages()
        self.button_back = ctk.CTkButton(self.main, text="Volver", command=self.view_menu)
        self.button_back.pack(padx=20, pady=20, side="bottom", anchor="e")

        new_page = page(self.main, self.auth)

        new_page.pack(fill="both", expand=True, )

        new_page.tkraise()

    def delete_pages(self):
        for widget in self.main.winfo_children():
            widget.destroy()
            widget.pack_forget()  # Quitamos todos los widgets del body

    # def change_appearance_mode_event(self, new_appearance_mode: str):
    #     self.storage.save("appearance_mode", new_appearance_mode)
    #     ctk.set_appearance_mode(new_appearance_mode)
    #
    # def change_scaling_event(self, new_scaling: str):
    #     new_scaling_float = int(new_scaling.replace("%", "")) / 100
    #     self.storage.save("scaling", new_scaling_float)
    #
    #     ctk.set_widget_scaling(new_scaling_float)
