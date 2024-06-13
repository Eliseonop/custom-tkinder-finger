# vistas/vista1.py

import customtkinter as ctk
from controladores.controlador_principal import ControladorPrincipal


class SubirTemplate(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # self.boton = ctk.CTkButton(self, text="Vista 1", command=self.destroy)
        # self.boton.pack(padx=20, pady=20)

        self.optionmenu = ctk.CTkOptionMenu(self, values=["option 1", "option 2"],
                                            )

        self.optionmenu.pack(padx=20, pady=20)
        # self.controlador = controlador
        # self.controlador.probar_dispositivo()
        # self.huellas = self.controlador.cargar_huellas()
        # # print(self.huellas)
        # if (self.huellas is None):
        #     print("No hay huellas")
        # else:
        #     for huella in self.huellas:
        #         print(huella)
        # # self.optionmenu.configure(values=list_huellas)

    def optionmenu_callback(choice):
        print("optionmenu dropdown clicked:", choice)
