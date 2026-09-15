import json
import re
from datetime import datetime

FILE_NAME = "asistencia.json"

def cargar_datos():
    """Lee el archivo JSON y retorna la lista de registros (diccionarios)."""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def Datos_personal(datos):
    """Guarda la lista de diccionarios en el archivo JSON."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def validar_formato_hora(hora):
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora))

def validar_id_empleado(emp_id):
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id))

def calcular_horas(entrada, salida):
    fmt = "%H:%M"
    t_entrada = datetime.strptime(entrada, fmt)
    t_salida = datetime.strptime(salida, fmt)
    diferencia = t_salida - t_entrada
    horas = diferencia.total_seconds() / 3600
    return round(horas, 2)

def obtener_nuevo_id(datos):
    return 1 if not datos else datos[-1]["id"] + 1

def buscar_registro_por_id(datos, reg_id):
    for r in datos:
        if r["id"] == reg_id:
            return r
    return None