# controladores/controlador_principal.py

from varios.vistas.vista1 import Vista1
from varios.vistas.vista2 import Vista2


class ControladorPrincipal:
    def __init__(self, app):
        self.app = app
        self.vistas = {
            "vista1": Vista1,
            "vista2": Vista2
        }

    def mostrar_vista(self, vista):
        if self.app.current_view:
            self.app.current_view.pack_forget()
        vista_clase = self.vistas[vista]
        self.app.current_view = vista_clase(self.app)
        self.app.current_view.pack(fill='both', expand=True)
