import customtkinter as ctk
from PIL import Image
import os
from servicios.auth import Auth


# from pages.autenticar import Autenticar


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, appearance_callback, scaling_callback, on_page_callback, button_info_list,
                 salir_callback):
        super().__init__(master, width=220, corner_radius=0)
        self.grid_rowconfigure(7, weight=1)
        self.master = master
        self.salir_callback = salir_callback
        self.auth = Auth()
        # image_path = os.path.join(os.path.dirname(__file__))
        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(50, 50))

        self.logo_label = ctk.CTkLabel(self,
                                       image=self.logo_image,
                                       text="",
                                       font=ctk.CTkFont(size=20, weight="bold"),
                                       compound="left")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Añadir la frase debajo del logo
        self.tagline_label = ctk.CTkLabel(self,
                                          text="Asistencia Planilla",
                                          font=ctk.CTkFont(size=15, weight="normal"),
                                          anchor="w")
        self.tagline_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Crear botones dinámicamente a partir de la lista de información
        for idx, button_info in enumerate(button_info_list):
            name = button_info["name"]
            vista = button_info["vista"]
            button = ctk.CTkButton(self, text=name, command=lambda v=vista: on_page_callback(v))
            button.grid(row=idx + 2, column=0, padx=20, pady=10)  # Ajustar el índice de fila

        self.appearance_mode_label = ctk.CTkLabel(self, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5 + len(button_info_list), column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self,
                                                             values=["Light", "Dark", "System"],
                                                             command=appearance_callback,
                                                             variable=ctk.StringVar(value="System"))
        self.appearance_mode_optionemenu.grid(row=6 + len(button_info_list), column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self, text="Escala UI :", anchor="w")
        self.scaling_label.grid(row=7 + len(button_info_list), column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self,
                                                     values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=scaling_callback,
                                                     variable=ctk.StringVar(value="100%")
                                                     )
        self.scaling_optionemenu.grid(row=8 + len(button_info_list), column=0, padx=20, pady=(10, 20))

        #         logout
        self.logout_button = ctk.CTkButton(self, text="Cerrar Sesión",
                                           command=self.logout
                                           )
        self.logout_button.grid(row=9 + len(button_info_list), column=0, padx=20, pady=(10, 20))

    def logout(self):
        self.salir_callback()

    def sidebar_button_event(self):
        print("Button clicked")
        pass
