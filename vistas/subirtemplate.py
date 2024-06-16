# vistas/vista1.py

import customtkinter as ctk
from tkinter import StringVar
from controladores.device import Device
from servicios.empleados import Empleados
from servicios.auth import Auth


class SubirTemplate(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        auth = Auth()
        auth.sign_in('username', 'password')  # Asegúrate de manejar el inicio de sesión correctamente
        empleados = Empleados(auth)

        self.listaEmpleados = empleados.obtener_empleados()

        if self.listaEmpleados:
            self.nombres_empleados = [empleado['nombre'] for empleado in self.listaEmpleados]
        else:
            self.nombres_empleados = ["No se encontraron empleados"]

        self.label = ctk.CTkLabel(self, text="Subir Huella Digital")
        self.label.pack(padx=20, pady=20)

        self.var = StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.var)
        self.entry.pack(padx=20, pady=2)
        self.entry.bind('<KeyRelease>', self.check_autocomplete)

        self.optionmenu_var = StringVar()
        self.optionmenu = ctk.CTkOptionMenu(self, variable=self.optionmenu_var, values=self.nombres_empleados)
        self.optionmenu.pack(padx=20, pady=20)

        self.update_optionmenu(self.nombres_empleados)

    def check_autocomplete(self, event):
        typed = self.var.get()
        if typed == '':
            data = self.nombres_empleados
        else:
            data = [item for item in self.nombres_empleados if typed.lower() in item.lower()]
        self.update_optionmenu(data)

    def update_optionmenu(self, data):
        # Clear current options
        self.optionmenu.configure(values=data)
        if data:
            self.optionmenu_var.set(data[0])
        else:
            self.optionmenu_var.set('')

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
