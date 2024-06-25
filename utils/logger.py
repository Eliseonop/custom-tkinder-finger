import json
from datetime import datetime


class Logger:
    def __init__(self, file_path="log.json"):
        self.file_path = file_path

    def save_log(self, data):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {"hora": current_time, "data": data}

        try:
            with open(self.file_path, "a") as file:
                json.dump(log_entry, file)
                file.write("\n")
            return True  # Éxito al guardar el log
        except Exception as e:
            print(f"Error al guardar el log: {e}")
            return False  # Error al guardar el log
