# vistas/vista1.py

import customtkinter as ctk


class Vista1(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master,fg_color="transparent")

        self.boton = ctk.CTkButton(self, text="Vista 1", command=self.destroy)
        self.boton.pack(padx=20, pady=20)
