import os
import sys


def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, trabajando para desarrollo y PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


RUTA_FAVICON = resource_path(os.path.join('assets', 'favicon.ico'))

RUTA_LOGO = resource_path(os.path.join('assets', 'logo.png'))
RUTA_FABRICACION = resource_path(os.path.join('assets', 'gear.png'))

RUTA_VERIFY = resource_path(os.path.join('assets', 'verify.png'))
RUTA_MARK = resource_path(os.path.join('assets', 'mark.png'))

RUTA_USER_ADD = resource_path(os.path.join('assets', 'user_add.png'))
RUTA_ERROR_RED = resource_path(os.path.join('assets', 'error.png'))
RUTA_SERVER = resource_path(os.path.join('assets', 'server.png'))