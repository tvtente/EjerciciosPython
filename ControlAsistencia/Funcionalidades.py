import time
from datetime import datetime

from BDD import cargar_datos, guardar_datos
from BorrarPantalla import Borro
from Validaciones import validar_formato_hora, validar_id_empleado


def calcular_horas(entrada, salida):
    """Calcula las horas trabajadas entre una entrada y una salida."""
    formato = "%H:%M"
    hora_entrada = datetime.strptime(entrada, formato)
    hora_salida = datetime.strptime(salida, formato)
    return round((hora_salida - hora_entrada).total_seconds() / 3600, 2)


def crear_registro():
    """Solicita los datos de un empleado y crea su registro de asistencia."""
    datos = cargar_datos()
    emp_id = input("ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(emp_id):
        print("❌ Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).❌")
        time.sleep(5)
        Borro()
        return

    nombre = input("Nombre del empleado: ").strip()
    if not nombre:
        print("❌ El nombre no puede estar vacío.")
        time.sleep(3)
        Borro()
        return

    fecha = datetime.now().strftime("%Y-%m-%d")
    entrada = input("Hora de entrada (HH:MM): ")
    if not validar_formato_hora(entrada):
        print("Formato de hora inválido. Use HH:MM.")
        return

    salida = input("Hora de salida (HH:MM, presione Enter si queda pendiente): ")
    horas_trabajadas = 0.0
    if salida:
        if not validar_formato_hora(salida):
            print("Formato de hora de salida inválido.")
            return
        horas_trabajadas = calcular_horas(entrada, salida)

    nuevo_id = 1 if not datos else datos[-1]["id"] + 1
    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "nombre": nombre,
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida if salida else "Pendiente",
        "horas_trabajadas": horas_trabajadas,
    }
    datos.append(registro)
    guardar_datos(datos)
    print("Registro guardado exitosamente.")


def leer_registros():
    """Muestra por pantalla todos los registros de asistencia guardados."""
    datos = cargar_datos()
    if not datos:
        print("No hay registros en el sistema.")
        time.sleep(5)
        Borro()
        return

    for registro in datos:
        print(
            f"ID: {registro['id']} | Empleado: {registro['empleado']} | "
            f"Nombre: {registro.get('nombre', 'Sin nombre')} | "
            f"Fecha: {registro['fecha']} | Entrada: {registro['entrada']} | "
            f"Salida: {registro['salida']} | Horas: {registro['horas_trabajadas']}"
        )


def actualizar_registro():
    """Modifica la entrada y salida de un registro indicado por su ID."""
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a actualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    for registro in datos:
        if registro["id"] == reg_id:
            print(f"Registro encontrado: {registro}")
            nueva_entrada = input(f"Nueva entrada [{registro['entrada']}]: ") or registro["entrada"]
            if not validar_formato_hora(nueva_entrada):
                print("Hora de entrada inválida.")
                return

            nueva_salida = input(f"Nueva salida [{registro['salida']}]: ") or registro["salida"]
            if nueva_salida != "Pendiente" and not validar_formato_hora(nueva_salida):
                print("Hora de salida inválida.")
                return

            registro["entrada"] = nueva_entrada
            registro["salida"] = nueva_salida
            registro["horas_trabajadas"] = (
                calcular_horas(nueva_entrada, nueva_salida)
                if nueva_salida != "Pendiente"
                else 0.0
            )
            guardar_datos(datos)
            print("Registro actualizado correctamente.")
            return

    print("Registro no encontrado.")


def eliminar_registro():
    """Elimina el registro que coincida con el ID introducido."""
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return

    nuevos_datos = [registro for registro in datos if registro["id"] != reg_id]
    if len(nuevos_datos) == len(datos):
        print("Registro no encontrado.")
        return

    guardar_datos(nuevos_datos)
    print("Registro eliminado correctamente.")
