import logging


class Logger:
    def __init__(self, file_path="app.log"):
        self.file_path = file_path
        logging.basicConfig(filename=self.file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def save_log_info(self, data):
        logging.info(data)
        return True

    def save_log_error(self, data):
        logging.error(data)
        return True

    def clear_log(self):
        try:
            open(self.file_path, 'w').close()  # Abre y cierra el archivo para borrar su contenido
            return True
        except Exception as e:
            print(f"Error al limpiar el log: {e}")
            return False
