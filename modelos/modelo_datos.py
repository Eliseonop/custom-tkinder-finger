class ModeloDatos:
    def __init__(self):
        self.datos = []

    def agregar_dato(self, dato):
        self.datos.append(dato)

    def obtener_datos(self):
        return self.datos
