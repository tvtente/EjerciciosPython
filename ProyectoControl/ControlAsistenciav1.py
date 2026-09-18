import json
import re
import time
import os
from datetime import datetime

FILE_NAME = "asistencia.json"

# --- CÓDIGOS DE COLORES ANSI ---
COLOR_ROJO = "\033[91m"
COLOR_AZUL = "\033[94m"
RESET_COLOR = "\033[0m"

ANCHO = 66  # Ancho fijo garantizado para que no se deforme el marco

def borrar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_datos():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(datos):
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

def imprimir_encabezado():
    borrar_pantalla()
    linea = "+" + "-" * (ANCHO - 2) + "+"
    print(linea)
    print("|" + " CONTROL DE ASISTENCIA ".center(ANCHO - 2) + "|")
    print("|" + " [ MARCACIONES Y REGISTRO ] ".center(ANCHO - 2) + "|")
    print(linea)

def pedir_hora(mensaje):
    while True:
        print(mensaje)
        hora_raw = input("  Formato (HH:MM) -> : ").strip()
        
        if validar_formato_hora(hora_raw):
            return hora_raw
            
        print(f"\n{COLOR_ROJO} [X] Error: use el formato HH:MM (ejemplo: 12:36).{RESET_COLOR}")
        time.sleep(1.5)

# --- CREAR REGISTRO AUTOMÁTICO Y CONTINUO ---
def crear_registro():
    while True:
        imprimir_encabezado()
        datos = cargar_datos()
        
        # Mensaje centrado exactamente con el ancho del cuadro
        msg = "[ MODO CONTINUO ] (Presione Enter para volver al menú)"
        print(f"\n{msg.center(ANCHO)}\n")
        
        # 1. Captura de ID de empleado
        while True:
            emp_id = input(" ID del empleado (ej. EMP001): ").upper().strip()
            
            # Presionar Enter en blanco regresa al menú principal
            if emp_id == "":
                return

            if validar_id_empleado(emp_id):
                break
            
            print(f"\n{COLOR_ROJO} [X] Error: ID inválido (debe ser 3 letras y 3 números).{RESET_COLOR}")
            time.sleep(1.5)
            imprimir_encabezado()
            print("\n [ MODO MARCACIÓN CONTINUA ] (Presione Enter en vacío para volver al menú)\n")

        fecha = datetime.now().strftime("%Y-%m-%d")
        
        # 2. Captura directa de la Hora de Entrada
        entrada = pedir_hora("\n Hora de Entrada:")

        nuevo_id = 1 if not datos else datos[-1]["id"] + 1

        # Registro con salida en 'Pendiente' por defecto automáticamente
        registro = {
            "id": nuevo_id,
            "empleado": emp_id,
            "fecha": fecha,
            "entrada": entrada,
            "salida": "Pendiente",
            "horas_trabajadas": 0.0
        }

        # Guardar en archivo JSON
        datos.append(registro)
        guardar_datos(datos)
        
        # 3. Confirmación de marcación exitosa en AZUL
        print(f"\n{COLOR_AZUL} [ok] Entrada registrada correctamente. ¡Gracias, {emp_id}!{RESET_COLOR}")
        time.sleep(2)  # Muestra el mensaje por 2s y queda listo inmediatamente para el siguiente personal

def leer_registros():
    imprimir_encabezado()
    datos = cargar_datos()
    
    if not datos:
        print(f"\n{COLOR_ROJO} [X] No hay registros en el sistema.{RESET_COLOR}")
    else:
        print("\n+" + "-"*5 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*9 + "+" + "-"*9 + "+" + "-"*8 + "+")
        print(f"| {'ID':<3} | {'Empleado':<10} | {'Fecha':<10} | {'Entrada':<7} | {'Salida':<7} | {'Horas':<6} |")
        print("+" + "-"*5 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*9 + "+" + "-"*9 + "+" + "-"*8 + "+")
        
        for r in datos:
            print(f"| {r['id']:<3} | {r['empleado']:<10} | {r['fecha']:<10} | {r['entrada']:<7} | {r['salida']:<7} | {r['horas_trabajadas']:<6} |")
        
        print("+" + "-"*5 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*9 + "+" + "-"*9 + "+" + "-"*8 + "+")
    
    input("\n Presione Enter para regresar al menú...")

def actualizar_registro():
    while True:
        imprimir_encabezado()
        datos = Datospersonal.Datos_personal()
        
        # Opción para salir si el usuario presiona Enter sin ingresar datos
        print(" [ Presione Enter sin escribir nada para volver al menú ]\n")
        
        entrada_id = input(" Ingrese el ID a actualizar: ").strip()
        
        # Permitir cancelar la operación y regresar al menú
        if entrada_id == "":
            return

        # Validar que sea un número entero
        try:
            reg_id = int(entrada_id)
        except ValueError:
            print(f"\n{COLOR_ROJO} [X] Error: ID inválido. Debe ingresar un número.{RESET_COLOR}")
            time.sleep(3)
            continue  # Reinicia el ciclo y vuelve a mostrar la pantalla de registro

        # Buscar el registro en la lista
        registro_encontrado = None
        for r in datos:
            if r["id"] == reg_id:
                registro_encontrado = r
                break

        # Si no se encuentra el registro
        if not registro_encontrado:
            print(f"\n{COLOR_ROJO} [X] Código no es correcto!.{RESET_COLOR}")
            time.sleep(3)
            continue  # Reinicia el ciclo y vuelve a pedir el ID

        # Si el registro fue encontrado, proceder con la edición
        r = registro_encontrado
        print(f"\n Registro actual: [{r['empleado']}] Entrada: {r['entrada']} | Salida: {r['salida']}")
        
        if input("\n ¿Modificar entrada? (s/n): ").lower() == 's':
            r['entrada'] = pedir_hora(" Nueva Entrada:")

        if input(" ¿Registrar/Modificar salida? (s/n): ").lower() == 's':
            r['salida'] = pedir_hora(" Nueva Salida:")

        if r['salida'] != "Pendiente":
            r['horas_trabajadas'] = calcular_horas(r['entrada'], r['salida'])

        guardar_datos(datos)
        print(f"\n{COLOR_AZUL} [ok] Registro actualizado.{RESET_COLOR}")
        time.sleep(2)
        return  # Sale de la función y regresa al menú principal

def eliminar_registro():
    imprimir_encabezado()
    datos = cargar_datos()
    
    try:
        reg_id = int(input("\n Ingrese el ID del registro a eliminar: "))
    except ValueError:
        print(f"\n{COLOR_ROJO} [X] Error: ID inválido.{RESET_COLOR}")
        time.sleep(2)
        return

    nuevos_datos = [r for r in datos if r["id"] != reg_id]
    
    if len(nuevos_datos) == len(datos):
        print(f"\n{COLOR_ROJO} [X] Registro no encontrado.{RESET_COLOR}")
        time.sleep(2)
    else:
        guardar_datos(nuevos_datos)
        print(f"\n{COLOR_ROJO} [-] Registro eliminado correctamente.{RESET_COLOR}")
        time.sleep(2)

def menu():
    linea = "+" + "-" * (ANCHO - 2) + "+"
    
    while True:
        imprimir_encabezado()
        print(linea)
        print("|  1. Registrar Entrada (Crear Marcación)".ljust(ANCHO - 1) + "|")
        print("|  2. Ver Registros de Asistencia (Leer)".ljust(ANCHO - 1) + "|")
        print("|  3. Actualizar Registro (Salida / Edición)".ljust(ANCHO - 1) + "|")
        print("|  4. Eliminar Registro".ljust(ANCHO - 1) + "|")
        print("|  5. Salir".ljust(ANCHO - 1) + "|")
        print(linea)
        
        opcion = input("\n Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer_registros()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            borrar_pantalla()
            break
        else:
            print(f"\n{COLOR_ROJO} [X] Opción inválida.{RESET_COLOR}")
            time.sleep(2)

if __name__ == "__main__":
    menu()
