class ControladorPrincipal:
    def __init__(self, vista_principal):
        self.vista_principal = vista_principal

    def show_main_view(self):
        self.vista_principal.show_main_view()
