# vistas/vista2.py

import customtkinter as ctk


class Vista2(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="Esta es la Vista 2")
        self.label.grid(padx=20, pady=20)
        self.destroy()

