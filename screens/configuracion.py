import customtkinter as ctk

class Configuracion(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Agregar elementos de configuración, por ejemplo, etiquetas, entradas, botones, etc.
        label_config = ctk.CTkLabel(self, text="Configuración")
        label_config.pack()

        # Botón para volver al Frame de Reloj
        boton_volver = ctk.CTkButton(self, text="Volver", command=self.volver_a_reloj)
        boton_volver.pack()

    def volver_a_reloj(self):
        # Llamar a la función en App para volver al Frame de Reloj
        self.master.view_clock()