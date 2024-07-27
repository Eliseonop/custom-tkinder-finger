from enum import Enum


class CodeResponse(Enum):
    SUCCESS = 1
    OFFLINE = 2
    ERROR = 3
    UNAUTHORIZED = 4
    VALIDATION_ERROR = 5

# class Huellas:
#     def __init__(self, id, empleado, template):
#         self.id = id
#         self.empleado = empleado
#         self.template = template
#
#     def __str__(self):
#         return f"{self.id} - {self.empleado} "
