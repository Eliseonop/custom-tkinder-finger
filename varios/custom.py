import customtkinter as ctk
from vistas.vista_principal import VistaPrincipal
from controladores.controlador_principal import ControladorPrincipal

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")

app = VistaPrincipal()
controlador = ControladorPrincipal(app)
app.set_controlador(controlador)
app.mainloop()

# from tkinter import Tk
#
# import customtkinter
# from customtkinter import *
#
# # root = customtkinter.CTk()
#
# customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("blue")
#
#
# class Custom(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#         # self._set_appearance_mode("System")
#         self.geometry("1024x640")
#         self.title("Custom")
#         self.panels()
#         self.first()
#
#     def panels(self):
#         self.barra_superior = customtkinter.CTkFrame(self, height=150, bg_color="blue")
#         self.barra_superior.pack(side=customtkinter.TOP, fill='both')
#
#         # self.menu_lateral = customtkinter.CTkFrame(self, width=300, bg_color="gray")
#         # self.menu_lateral.pack(side=customtkinter.LEFT)
#         #
#         # self.contenido = customtkinter.CTkFrame(self, width=150,bg_color="blush")
#         # self.contenido.pack(side=customtkinter.RIGHT)
#
#     def hello(self):
#         self.label.configure(text=self.button.cget("text"))
#
#     def first(self):
#         # Use CTkButton instead of tkinter Button
#
#         self.button = customtkinter.CTkButton(self, text="Hola mundo!!",
#                                               command=self.hello,
#                                               height=40, width=100,
#                                               font=("Roboto", 12))
#         self.button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
#
#         self.label = customtkinter.CTkLabel(master=self, text="a")
#         self.label.pack(pady=1)
#
#
# app = Custom()
# app.mainloop()
