import os
import subprocess


def create_executable(script_name, output_name, icon_path=None, additional_data=None, hidden_imports=None,
                      no_console=False, output_dir='output'):
    """
    Crea un ejecutable usando PyInstaller.

    :param script_name: El nombre del script de Python a empaquetar.
    :param output_name: El nombre del ejecutable resultante.
    :param icon_path: Ruta al archivo de icono (.ico) (opcional).
    :param additional_data: Lista de datos adicionales a incluir en el formato "src;dest" (opcional).
    :param hidden_imports: Lista de módulos adicionales a importar (opcional).
    :param no_console: Si es True, elimina la consola para aplicaciones de GUI (opcional).
    :param output_dir: Directorio de salida para el ejecutable (opcional).
    """

    # Construir el comando básico de PyInstaller
    command = [
        'pyinstaller',
        '--onefile',
        '--name', output_name,
        '--distpath', output_dir
    ]

    # Agregar la opción de icono si se proporciona
    if icon_path:
        command.extend(['--icon', icon_path])

    # Agregar datos adicionales si se proporcionan
    if additional_data:
        for data in additional_data:
            command.extend(['--add-data', data])

    # Agregar importaciones ocultas si se proporcionan
    if hidden_imports:
        for hidden_import in hidden_imports:
            command.extend(['--hidden-import', hidden_import])

    # Agregar la opción de eliminar consola si se especifica
    if no_console:
        command.append('--noconsole')

    # Agregar el nombre del script al final del comando
    command.append(script_name)

    # Ejecutar el comando
    subprocess.run(command)


# Ejemplo de uso del script
if __name__ == "__main__":
    script_name = 'main.py'
    output_name = 'asistencia'
    icon_path = 'favicon.ico'
    additional_data = ['dlls/libzkfpcsharp.dll;.',
                       'assets;assets']  # Incluye la DLL desde la carpeta dlls y la carpeta de assets
    # hidden_imports = ['modulo_1', 'modulo_2']
    no_console = True
    output_dir = 'setup'  # Define la carpeta de salida personalizada

    create_executable(
        script_name=script_name,
        output_name=output_name,
        icon_path=icon_path,
        additional_data=additional_data,
        no_console=no_console,
        output_dir=output_dir)
