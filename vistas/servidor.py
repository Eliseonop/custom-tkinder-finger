import customtkinter as ctk
import threading
from servicios.empresa_service import EmpresaService
from tkinter import StringVar
from PIL import Image
from servicios.auth import Auth

class Servidor(ctk.CTkFrame):
    def __init__(self, master, auth: Auth):
        super().__init__(master)
        self.auth = auth
        self.urbanito_service = EmpresaService()
        self.progress_bar = ctk.CTkProgressBar(self, width=800, height=5)
        self.progress_bar.pack(side="top", pady=1, fill="x")
        self.initialize_ui_elements()
        self.load_empresas()

    def load_empresas(self):
        self.load_empresas_thread = threading.Thread(target=self.load_empresas_thread, daemon=True)
        self.load_empresas_thread.start()

    def display_message(self, message, pady=20):
        label = ctk.CTkLabel(self, text=message)
        label.pack(padx=20, pady=pady)

    def load_empresas_thread(self):
        # self.progress_bar.configure(mode="indeterminate", height=5)
        self.progress_bar.start()

        if self.urbanito_service.get_empresas():
            self.empresas = self.urbanito_service.empresas

            demo_empresa = {
                "id": 0,
                "codigo": "backend-planilla",
                "nombre": "Demo Planilla"
            }

            self.empresas.insert(0, demo_empresa)

            self.filtered_empresas = self.empresas
            self.selected_empresa = self.urbanito_service.get_empresa_storage()
            self.initialize_main_template()
        else:
            print("No se encontraron empresas")
            self.display_message("No se encontraron empresas")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def initialize_ui_elements(self):

        self.label_buscar = ctk.CTkLabel(self, text="Buscar Empresa")
        self.label_buscar.pack(padx=20, pady=2)

        self.var = StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.var)
        self.entry.pack(padx=20, pady=2)
        self.entry.bind('<KeyRelease>', self.check_autocomplete)

    def initialize_main_template(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scrollable_frame.pack(padx=20, pady=10)
        self.create_table_empresas()

    def create_table_empresas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Nombre", "Codigo", "Seleccionada", "Acciones"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        for i, empresa in enumerate(self.filtered_empresas, start=1):
            label_nombre = ctk.CTkLabel(self.scrollable_frame, text=empresa["nombre"], width=20, anchor="w")
            label_nombre.grid(row=i, column=0, padx=5, pady=5)
            label_ruc = ctk.CTkLabel(self.scrollable_frame, text=empresa["codigo"], width=20, anchor="w")
            label_ruc.grid(row=i, column=1, padx=5, pady=5)

            if self.selected_empresa and self.selected_empresa["codigo"] == empresa["codigo"]:

                my_image = ctk.CTkImage(light_image=Image.open("verify.png"),
                                        dark_image=Image.open("verify.png"),
                                        size=(25, 25))

                selected_label = ctk.CTkLabel(self.scrollable_frame, image=my_image, width=20,
                                              text="",
                                              anchor="w")
            else:
                my_image = ctk.CTkImage(light_image=Image.open("mark.png"),
                                        dark_image=Image.open("mark.png"),
                                        size=(20, 20))
                selected_label = ctk.CTkLabel(self.scrollable_frame, text="", width=20, anchor="w"
                                              , image=my_image)

            selected_label.grid(row=i, column=2, padx=5, pady=5)

            select_button = ctk.CTkButton(self.scrollable_frame, text="Seleccionar",
                                          command=lambda e=empresa: self.select_empresa(e))
            select_button.grid(row=i, column=3, padx=5, pady=5)

    def select_empresa(self, empresa):
        self.urbanito_service.save_empresa_storage(empresa)
        self.selected_empresa = empresa
        self.create_table_empresas()

    def check_autocomplete(self, event):
        search_term = self.var.get()
        self.filtered_empresas = [empresa for empresa in self.empresas if
                                  search_term.lower() in empresa["nombre"].lower()]
        self.create_table_empresas()
