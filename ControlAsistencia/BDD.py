import json
from pathlib import Path


FILE_NAME = Path(__file__).with_name("asistencia.json")


def cargar_datos():
    """Carga los registros guardados en el archivo JSON."""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_datos(datos):
    """Guarda la lista de registros en el archivo JSON."""
    with open(FILE_NAME, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
