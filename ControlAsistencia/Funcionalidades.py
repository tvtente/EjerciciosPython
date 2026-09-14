import time
from datetime import datetime

from BDD import cargar_datos, guardar_datos
from BorrarPantalla import Borro
from Validaciones import validar_formato_hora


def calcular_horas(entrada, salida):
    """Calcula las horas trabajadas entre una entrada y una salida."""
    formato = "%H:%M"
    hora_entrada = datetime.strptime(entrada, formato)
    hora_salida = datetime.strptime(salida, formato)
    return round((hora_salida - hora_entrada).total_seconds() / 3600, 2)


def crear_registro():
    """Solicita los datos de un empleado y crea su registro de asistencia."""
    datos = cargar_datos()

    # SOLO 6 empleados válidos
    empleados_validos = {
        "001": "Oksana Marcos",
        "002": "Italo Sherman",
        "003": "Gustavo Vladimir",
        "004": "Lindey García",
        "005": "Sanjana Kumari",
        "006": "Cristina Espacio"
    }

    # El usuario solo escribe el número
    numero = input("Número del empleado (001–006): ").strip()

    # Validación del número
    if numero not in empleados_validos:
        print("❌ Este número no existe. Solo hay 6 empleados registrados.")
        time.sleep(3)
        Borro()
        return

    # Generación automática del ID
    emp_id = f"EMP{numero}"

    # Nombre automático (NO se puede modificar)
    nombre = empleados_validos[numero]

    fecha = datetime.now().strftime("%d-%m-%y")

    #VALIDACIÓN DE HORA DE ENTRADA (CON AUTO-FORMATO Y BORRO)
    while True:
        entrada = input("Hora de entrada (HH:MM): ").strip()

        # Si escribe 4 números seguidos → convertir a HH:MM
        if entrada.isdigit() and len(entrada) == 4:
            entrada = entrada[:2] + ":" + entrada[2:]

        if validar_formato_hora(entrada):
            break

        print("❌ Formato de hora inválido. Use HH:MM.")
        time.sleep(3)
        Borro()

    #VALIDACIÓN DE HORA DE SALIDA (CON AUTO-FORMATO Y BORRO)
    horas_trabajadas = 0.0
    while True:
        salida = input("Hora de salida (HH:MM, Enter si queda pendiente): ").strip()

        # Si queda pendiente
        if salida == "":
            salida = "Pendiente"
            horas_trabajadas = 0.0
            break

        # Si escribe 4 números seguidos → convertir a HH:MM
        if salida.isdigit() and len(salida) == 4:
            salida = salida[:2] + ":" + salida[2:]

        if validar_formato_hora(salida):
            horas_trabajadas = calcular_horas(entrada, salida)
            break

        print("❌ Formato de hora inválido. Use HH:MM.")
        time.sleep(3)
        Borro()

    nuevo_id = 1 if not datos else datos[-1]["id"] + 1

    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "nombre": nombre,  # AUTOMÁTICO
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida,
        "horas_trabajadas": horas_trabajadas,
    }

    datos.append(registro)
    guardar_datos(datos)
    print(f"✔ Registro guardado exitosamente para {emp_id} ({nombre}).")



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
    datos = cargar_datos()     # Cargamos los datos
    try:
        reg_id = int(input("Ingrese el ID del registro a eliminar: "))   # Pedimos el ID del registro
    except ValueError:
        print("ID inválido.")   # Si no es un número, mostramos un error
        return

    nuevos_datos = [registro for registro in datos if registro["id"] != reg_id]   # Creamos una lista sin el registro elegido
    if len(nuevos_datos) == len(datos):   # Comprobamos si el registro existe
        print("Registro no encontrado.")
        return
    
    confirmar = input("¿Está seguro de eliminar este registro? (s/n): ").lower()  # Pedimos confirmación antes de eliminar
    
    if confirmar == "s":
        guardar_datos(nuevos_datos)  # Guardamos los datos sin el registro
        print("Registro eliminado correctamente.")
        
    else:
        print("Eliminación cancelada.")   # Cancelamos la eliminación
