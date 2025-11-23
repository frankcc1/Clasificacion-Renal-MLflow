# Importa el módulo 'os' que permite interactuar con el sistema operativo:
# crear carpetas, verificar archivos, obtener tamaños, etc.
import os
# Importa la clase Path de 'pathlib', que sirve para manejar rutas
# de forma más ordenada y compatible entre sistemas operativos.
from pathlib import Path
# Importa el módulo 'logging', usado para imprimir mensajes informativos
# con hora, nivel y formato profesional.
import logging
# Configura el sistema de logs:
# - level=logging.INFO → muestra mensajes informativos
# - format='[%(asctime)s]: %(message)s:' → muestra la hora y el mensaje
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')
# Nombre del proyecto, usado dinámicamente para construir rutas dentro de src/
project_name = 'cnnClassifier'
# Lista de rutas de archivos que queremos crear para estructurar el proyecto.
# Cada línea representa un archivo (y sus carpetas) que deben existir.
list_of_files = [
    ".github/workflows/.gitkeep",                     # Permite que Git mantenga carpetas vacías
    f"src/{project_name}/__init__.py",                # Convierte la carpeta en paquete de Python
    f"src/{project_name}/components/__init__.py",     # Submódulo del proyecto
    f"src/{project_name}/utils/__init__.py",          # Archivo para utilidades
    f"src/{project_name}/config/__init__.py",         # Archivo base para configuraciones
    f"src/{project_name}/config/configuration.py",    # Lógica para manejar configuraciones
    f"src/{project_name}/pipeline/__init__.py",       # Módulo para pipelines de procesamiento
    f"src/{project_name}/entity/__init__.py",         # Definición de entidades/clases del proyecto
    f"src/{project_name}/constants/__init__.py",      # Archivo para constantes globales
    "config/config.yaml",                             # Archivo de configuración externa
    "dvc.yaml",                                       # Configuración para DVC
    "params.yaml",                                    # Parámetros de modelo/experimentos
    "requirements.txt",                               # Lista de librerías a instalar
    "setup.py",                                       # Archivo para instalar el paquete
    "research/trials.ipynb",                          # Notebook para pruebas y análisis
    "templates/index.html"                            # Archivo HTML de ejemplo
]
# Recorre uno por uno los archivos de la lista
for filepath in list_of_files:   
    # Convierte la ruta (string) en un objeto Path para manejarla mejor
    filepath = Path(filepath)
    # Separa la ruta en:
    # - filedir: carpeta contenedora
    # - filename: nombre del archivo
    filedir, filename = os.path.split(filepath)
    # Si el archivo pertenece a una carpeta (filedir no vacío)
    # entonces se crea la carpeta, si es que no existía.
    if filedir != "":
        # Crea la carpeta y las subcarpetas necesarias.
        # exist_ok=True evita errores si ya existe.
        os.makedirs(filedir, exist_ok=True)
        # Mensaje de log indicando que se creó/verificó la carpeta.
        logging.info(f"Creating directory: {filedir} for the file: {filename}")
    # Verifica si el archivo NO existe, o si existe pero está vacío.
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        # Abre el archivo en modo escritura ("w").
        # - Si no existe, lo crea.
        # - Si existe, lo vacía.
        with open(filepath, "w") as f:
            pass  # No se escribe contenido, queda vacío.
        # Log indicando que el archivo vacío ha sido creado.
        logging.info(f"Creating empty file: {filepath}")
    else:
        # Si el archivo ya existe y tiene contenido, no se hace nada.
        logging.info(f"{filename} already exists")
