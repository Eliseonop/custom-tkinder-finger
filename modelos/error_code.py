from enum import Enum


class ErrorCode(Enum):
    SUCCESS = 1
    OFFLINE = 2
    ERROR = 3

# class Huellas:
#     def __init__(self, id, empleado, template):
#         self.id = id
#         self.empleado = empleado
#         self.template = template
#
#     def __str__(self):
#         return f"{self.id} - {self.empleado} "