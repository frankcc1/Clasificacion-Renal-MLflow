import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64



@ensure_annotations # ← Verifica que el tipo del argumento sea correcto en tiempo de ejecución
def read_yaml(path_to_yaml: Path) -> ConfigBox: 
    """Lee un archivo YAML y lo convierte en ConfigBox (acceso con .)"""
    try:
        with open(path_to_yaml) as yaml_file: # Abre el yaml en modo lectura
            content = yaml.safe_load(yaml_file) # Carga el contenido del yaml
            logger.info(f"yaml file: {path_to_yaml} loaded successfully") # Log: Avisa que todo salio bien
            return ConfigBox(content) # Convierte el diccionario en ConfigBox
    except BoxValueError: # Error si el yaml esta vacio o tiene un error
        raise ValueError("yaml file is empty") # Lanza error para saber que paso
    except Exception as e: # Avisa cualquier otro error
        raise e # Lo reelanza para evitar perder el mensaje original
    


@ensure_annotations #Esto verifica que la entrada de la funcion 
                    #el primer elemento sea una lista y la segunda verbose sea bool
def create_directories(path_to_directories: list, verbose=True):
    """Crea una lista de directorios de forma segura.
    
    Args:
        path_to_directories (list): lista de rutas (pueden ser str o Path)
        verbose (bool): si True, escribe un log cada vez que crea una carpeta
    """
    for path in path_to_directories:   # Recorre cada ruta de la lista 
        os.makedirs(path, exist_ok=True) # Crea carpetas y subcarpetas, si ya existe no error
        if verbose: 
            logger.info(f"created directory at: {path}") #Si verbose es V, se crea el log para tener un registro de lo creado


@ensure_annotations #Asegura que la entrada sea tipo path y data sea diccionario
def save_json(path: Path, data: dict):
    """
        Guarda un diccionario como archivo JSON con formato legible (indentado)
    """
    with open(path, "w") as f:   #Abre o crea un archivo en modo lectura
        json.dump(data, f, indent=4) # Escribe el diccionario como Json
                                     # indent = 4, para hacerlo legible y bonito xD

    logger.info(f"json file saved at: {path}") # Log: Confirma que se guardó y dónde se guardó




@ensure_annotations # Verifica que 'path' sea tipo Path y que devuelva ConfigBox
def load_json(path: Path) -> ConfigBox:
    """
    Carga un archivo JSON y lo convierte en ConfigBox (acceso con punto)
    """
    with open(path) as f: # Abre el archivo json en modo lectura
        content = json.load(f) # Lee y convierte el Json en diccionario

    logger.info(f"json file loaded succesfully from: {path}") # Log: Confirma que todo salio bien
    return ConfigBox(content) # Convierte el diccionario en ConfigBox (Para acceder a objetos mediante un punto ".")


'''
Esta función guarda cualquier objeto de Python (modelo entrenado, pipeline, 
transformador, scaler, diccionario grande, etc.) en un archivo binario eficiente 
usando joblib, y registra en el log dónde se guardó.
'''
@ensure_annotations # Verifica que 'data' sea cualquier tipo y 'path' sea Path
def save_bin(data: Any, path: Path):
    """
    Guarda cualquier objeto Python como archivo binario usando joblib
    """
    joblib.dump(value=data, filename=path) #Guarda el objeto en formato binario
                                           #Joblib es más rápido que pickle
    logger.info(f"binary file saved at: {path}") # Log: Confirma que el objeto se guardo bien


@ensure_annotations
def load_bin(path: Path) -> Any: # ecibe una ruta (Path) y devuelve cualquier tipo de objeto (Any)
    """
    Carga datos binarios desde un archivo (Traducción sintetizada)

    Args:
        path (Path): ruta al archivo binario

    Returns:
        Any: el objeto recuperado que estaba guardado en el archivo
    """
    data = joblib.load(path) # Lee el archivo binario desde el disco y reconstruye el objeto en memoria
    logger.info(f"binary file loaded from: {path}") # Registra en el log
    return data # Devuelve el objeto

@ensure_annotations
def get_size(path: Path) -> str:
    """Obtiene el tamaño de un archivo en KB (Traducción sintetizada)

    Args:
        path (Path): ruta del archivo

    Returns:
        str: tamaño en KB
    """
    size_in_kb = round(os.path.getsize(path)/1024) # Se obtiene bytes pero se divide entre 1024 para 
                                                   # transformarlos a Kb
    return f"~ {size_in_kb} KB" # Devuelve tamaño en KB en string


def decodeImage(imgstring, fileName): # Recibe el texto base64 y el nombre del archivo final
    imgdata = base64.b64decode(imgstring) # Decodifica la cadena de texto base64 a bytes
    with open(fileName, 'wb') as f: # Abre (o crea) el archivo en modo 'Escritura Binaria' (wb)
        f.write(imgdata) # Escribe los datos binarios decodificados dentro del archivo
        f.close() # Cerrando el archivo


def encodeImageIntoBase64(croppedImagePath): # Recibe la imagen a procesar 
    with open(croppedImagePath, "rb") as f: # Abre el archivo en binario
        return base64.b64encode(f.read()) # Lee la imagen y lo convierte a Base64