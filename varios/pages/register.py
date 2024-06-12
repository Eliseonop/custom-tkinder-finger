import customtkinter as ctk


class Register(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.boton = ctk.CTkButton(self, text="Register", command=self.destroy)
        self.boton.pack(padx=20, pady=20)
