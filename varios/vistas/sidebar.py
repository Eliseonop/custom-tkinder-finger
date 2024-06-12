import customtkinter as ctk
from PIL import Image
import os
from config import GRAY, BLUSH, ONYX, NON_BLUE, ROBIN_BLUE, SIDE_BAR
from varios.vistas.vista1 import Vista1


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, appearance_callback, scaling_callback, on_page_callback, button_info_list):
        super().__init__(master, width=180, corner_radius=0)
        self.grid_rowconfigure(4, weight=1)

        image_path = os.path.join(os.path.dirname(__file__), "../../utils")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(50, 50))

        self.logo_label = ctk.CTkLabel(self,
                                       image=self.logo_image,
                                       text="",
                                       font=ctk.CTkFont(size=20, weight="bold"),
                                       compound="left")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Crear botones dinámicamente a partir de la lista de información
        for idx, button_info in enumerate(button_info_list):
            name = button_info["name"]
            vista = button_info["vista"]
            button = ctk.CTkButton(self, text=name, command=lambda v=vista: on_page_callback(v))
            button.grid(row=idx + 1, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self,
                                                             values=["Light", "Dark", "System"],
                                                             command=appearance_callback,
                                                             variable=ctk.StringVar(value="System"))
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self, text="Escala UI :", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self,
                                                     values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=scaling_callback,
                                                     variable=ctk.StringVar(value="100%")
                                                     )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    def sidebar_button_event(self):
        print("Button clicked")
        pass
