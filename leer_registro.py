import json
import time
from BorroPantalla import Borro


FILE_NAME = "asistencia.json"


def cargar_datos():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    def leer_registro():
        datos = cargar_datos()

        # Comprobamos si existen registros
        if not datos:
            print("\n" + "=" * 60)
            print("                REGISTROS DE ASISTENCIA")
            print("=" * 60)
            print("\n No hay registros en el sistema.")

            time.sleep(3)
            Borro()
            return

        # Encabezado
        print("\n" + "=" * 60)
        print("                REGISTROS DE ASISTENCIA")
        print("=" * 60)

        # Mostrar todos los registros
        for r in datos:
            print(f"""
            ID del registro: {r['id']}
            Empleado: {r['empleado']}
            Fecha: {r['fecha']}
            Entrada: {r['entrada']}
            Salida: {r['salida']}
            Horas trabajadas: {r['horas_trabajadas']}
            {"-" * 60}""")
            
            # Total de registros
            print(f"total de registros: {len(datos)}")

            # Esperar antes de volver al menu
            input("\nPresione Enter para volver al menú...")
            Borro()