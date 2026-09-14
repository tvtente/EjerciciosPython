import json
import time
from BorrarPantalla import Borro

FILE_NAME = "asistencia.json"


def cargar_datos():
    """Carga los registros desde el archivo JSON anterior."""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def leer_registros():
    """Muestra los registros con el formato antiguo del archivo."""
    datos = cargar_datos()

    if not datos:
        print("\n" + "=" * 60)
        print("           REGISTROS DE ASISTENCIA")
        print("=" * 60)
        print("\nNo hay registros en el sistema.")

        time.sleep(3)
        Borro()
        return

    print("\n" + "=" * 60)
    print("           REGISTROS DE ASISTENCIA")
    print("=" * 60)

    for r in datos:
        print(f"""
ID del registro : {r['id']}
Empleado        : {r['empleado']}
Nombre          : {r['nombre']}
Fecha           : {r['fecha']}
Entrada         : {r['entrada']}
Salida          : {r['salida']}
Horas trabajadas: {r['horas_trabajadas']}
{"-" * 60}""")

    print(f"Total de registros: {len(datos)}")

    input("\nPresione ENTER para volver al menú...")

    Borro()
