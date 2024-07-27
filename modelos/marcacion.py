class Marcacion:
    def __init__(self, data):
        self.id = data.get('id')
        self.hora = data.get('hora')
        self.manual = data.get('manual')
        self.entrada = data.get('entrada')
